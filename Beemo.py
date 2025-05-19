#!/usr/bin/env python3
import sounddevice as sd
import json
import queue
import sys
import threading
import select
import termios
import tty
import re
import requests
from vosk import Model, KaldiRecognizer
from TTS.api import TTS

# ─── SETTINGS ──────────────────────────────────────────────
PERSONALITY = (
    "You are BeeMO, a chill and laid-back assistant. "
    "You are great at math and factual answers. "
    "You never use stage directions, emotions, or asides. "
    "Always end your response with: 'I AM THE KING OF THE WORLD'."
)
VOSK_MODEL_DIR = "./vosk-model-small-en-us-0.15"
SAMPLERATE = 16000
BLOCKSIZE = 8000

# ─── AUDIO OUTPUT (COQUI TTS) ──────────────────────────────
tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=False)
default_speaker = tts.speakers[0]

def speak(text: str):
    wav = tts.tts(text, speaker=default_speaker, speed=1.25)
    sd.play(wav, samplerate=tts.synthesizer.output_sample_rate)
    sd.wait()

# ─── CONVERSATION STATE ────────────────────────────────────
history = [{"role": "system", "content": PERSONALITY}]
q = queue.Queue()

# ─── LLM CALL ───────────────────────────────────────────────
def ask_bot(user_text: str):
    global history
    history.append({"role": "user", "content": user_text})

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3",
            "messages": history,
            "stream": False
        }
    )

    reply = response.json()["message"]["content"]
    history.append({"role": "assistant", "content": reply})

    reply = re.sub(r'^BeeMO:\s*', '', reply.strip(), flags=re.IGNORECASE)
    return reply

# ─── AUDIO INPUT ────────────────────────────────────────────
def audio_callback(indata, frames, time, status):
    if status:
        print("⚠️ Audio status:", status, file=sys.stderr)
    q.put(bytes(indata))

def recognize_loop():
    rec = KaldiRecognizer(Model(VOSK_MODEL_DIR), SAMPLERATE)
    global history
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            user = json.loads(rec.Result()).get("text", "").strip()
            if user:
                print(f"\n👤 You said: {user}")
                if user.lower() == "reset memory":
                    history = [{"role": "system", "content": PERSONALITY}]
                    print("🧠 Memory reset.")
                    speak("Memory has been reset. I AM THE KING OF THE WORLD")
                    continue
                resp = ask_bot(user)
                print(f"🤖 Bot says: {resp}\n")
                speak(resp)

# ─── MANUAL MODE (VISIBLE INPUT + EXIT W/ 4) ───────────────
def handle_manual_input(stream=None, old_tty_attrs=None):
    global history

    if stream:
        stream.stop()

    while not q.empty():
        try:
            q.get_nowait()
        except queue.Empty:
            break

    # Turn echo ON
    termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_tty_attrs)

    while True:
        try:
            user = input("\n⌨️ Type message (or '4' alone to return to voice): ").strip()
        except EOFError:
            continue

        if user == "4":
            print("🔁 Returning to voice input mode...")
            tty.setcbreak(sys.stdin.fileno())  # restore no-echo mode
            if stream:
                stream.start()
            break
        elif user:
            print(f"👤 You typed: {user}")
            if user.lower() == "reset memory":
                history = [{"role": "system", "content": PERSONALITY}]
                print("🧠 Memory reset.")
                speak("Memory has been reset. I AM THE KING OF THE WORLD")
            else:
                resp = ask_bot(user)
                print(f"🤖 Bot says: {resp}\n")
                speak(resp)

# ─── MAIN LOOP ─────────────────────────────────────────────
if __name__ == "__main__":
    print("Select listening mode:")
    print("  1: Continuous listening (bot always listens)")
    print("  2: Push-to-talk        (SPACE=listen, 3=type, 4=exit manual)")
    choice = input("Enter 1 or 2: ").strip()
    continuous = (choice == "1")
    print(f"✅ Mode selected: {'Continuous' if continuous else 'Push-to-Talk'}\n")

    fd = sys.stdin.fileno()
    old_tty_attrs = termios.tcgetattr(fd)
    tty.setcbreak(fd)

    try:
        stream = sd.RawInputStream(
            samplerate=SAMPLERATE,
            blocksize=BLOCKSIZE,
            dtype="int16",
            channels=1,
            callback=audio_callback
        )

        threading.Thread(target=recognize_loop, daemon=True).start()

        if continuous:
            stream.start()
            print("🔊 Listening continuously… (Ctrl-C to quit)")
            while True:
                sd.sleep(1000)

        else:
            listening = False
            stream_started = False
            print("🔈 Push-to-Talk mode:")
            print("    • Press SPACE to start/stop listening")
            print("    • Press 3 to type a corrected input manually")
            print("    • Type '4' while typing to return to voice mode\n")

            while True:
                dr, _, _ = select.select([sys.stdin], [], [], 0.1)
                if dr:
                    key = sys.stdin.read(1)
                    if key == " ":
                        if not stream_started:
                            stream.start()
                            stream_started = True
                            listening = True
                            print("🔊 Listening… (press SPACE to pause)")
                        else:
                            stream.stop()
                            stream_started = False
                            listening = False
                            print("⏸️ Listening paused (press SPACE to resume)")

                    elif key == "3":
                        if stream_started:
                            stream.stop()
                            stream_started = False
                            listening = False
                            print("⏸️ Paused listening to enter manual input")
                        handle_manual_input(stream=stream, old_tty_attrs=old_tty_attrs)

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_tty_attrs)
        if 'stream' in locals() and stream.active:
            stream.stop()
        if 'stream' in locals():
            stream.close()
