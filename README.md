# BeeMo – A Local AI Voice Assistant with Memory, Typing Mode, and TTS  
*By Christian McGowan*

BeeMo is a fully offline, privacy-respecting voice assistant developed as a personal project. Designed to act as a responsive and context-aware conversational agent, BeeMo uses open-source tools to provide speech recognition, intelligent responses, and realistic voice synthesis — all without sending a single byte to the cloud.

Whether you're experimenting with LLMs, building secure tools, or just want a fun voice bot that works without surveillance, BeeMo is built for you.

---

## 🧠 Key Features

- **Completely Offline** – No internet connection required once set up.
- **Conversational Memory** – Maintains context throughout a session.
- **Push-to-Talk & Typing Support** – Speak or type your input seamlessly.
- **Realistic Voice Output** – Coqui TTS makes BeeMo sound natural and expressive.
- **Backed by LLaMA 3** – Uses `llama3` via Ollama for local, intelligent responses.
- **Correction Mode** – Press a key to override misheard speech manually.
- **Keyboard Controls** – Optimized for hands-on interaction and full control.

---

## ⚙️ Requirements

### 🧱 Core Software

- **Python 3.8+**
- [**Ollama**](https://ollama.com) installed and running `llama3` or `mistral`
- [**Vosk**](https://alphacephei.com/vosk) English voice recognition model

### 🐍 Python Dependencies (via `requirements.txt`)

```
sounddevice
vosk
TTS
requests
```

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/BeeMo.git
cd BeeMo
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python Requirements

```bash
pip install -r requirements.txt
```

### 4. Start Ollama and Load the Model

Install Ollama from [https://ollama.com](https://ollama.com), then:

```bash
ollama pull llama3
ollama run llama3
```

### 5. Download the Vosk Speech Model

```bash
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
```

Move the extracted folder into your project:

```
BeeMo/vosk-model-small-en-us-0.15/
```

---

## 🚀 Running BeeMo

Once everything is installed, run the assistant:

```bash
python3 BeeMo.py
```

You will be prompted to select a listening mode:

- `1` – Continuous Voice Listening
- `2` – Push-to-Talk Mode

---

## 🕹️ Controls & Commands

### In Push-to-Talk Mode:

| Key | Function |
|-----|----------|
| `SPACE` | Toggle listening on/off |
| `3` | Enter manual typing mode |
| `4` | Exit typing mode and resume voice input |
| `Ctrl + C` | Exit the program |

### Spoken or Typed Phrases:

- `reset memory` — Clears all chat history

---

## 🧾 Project Layout

```
BeeMo/
├── BeeMo.py                    # Main voice assistant script
├── requirements.txt            # Required Python packages
├── README.md                   # This file
├── vosk-model-small-en-us-0.15/  # Downloaded separately (not uploaded)
```

---

## 🔐 Privacy Notice

BeeMo is entirely local.  
No data, input, or audio ever leaves your machine.  
All voice recognition, model inference, and synthesis occur on-device using open-source tools. This makes BeeMo suitable for personal, academic, and private offline use cases.

---

## ❗ Known Limitations

- TTS playback is not streamed in real time (plays after generation).
- Model responses are not filtered — BeeMo is as powerful and unpredictable as your local LLM.
- Voice recognition accuracy may degrade in loud environments.

---

## 🧩 Future Ideas

- Add GUI mode using PyQt or Tkinter
- Hotword wake-up (e.g. “Hey BeeMo”)
- Optional streaming TTS playback
- Log history to disk

---

## 🧑‍💻 Author

**Christian McGowan**  
Computer Science (Cybersecurity Track)  
California State University, Fullerton  
🐙 GitHub: [@Christian-McGowan](https://github.com/Christian-McGowan)

---

## 📜 License

This project is released under the **MIT License**.  
Feel free to fork, improve, or integrate it into your own offline agents.

---

> “I AM THE KING OF THE WORLD.”
