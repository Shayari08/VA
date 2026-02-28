# JARVIS — AI-Powered Voice Assistant

> A Python-based voice-activated personal assistant with speech recognition, text-to-speech synthesis, real-time API integrations, and AI-powered PDF document analysis via a Streamlit web interface.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Voice Commands](#voice-commands)
- [API Integrations](#api-integrations)
- [Project Structure](#project-structure)
- [Known Limitations](#known-limitations)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

JARVIS is a dual-mode AI assistant:

1. **Voice Assistant Mode** — Listens for spoken commands, performs OS-level tasks, queries external APIs (weather, news, Wikipedia, movies), sends emails, controls YouTube, and more — then speaks the response back.
2. **Document Chat Mode** — A Streamlit web app that ingests PDF files, indexes them with FAISS vector search, and lets you converse with the content using a Retrieval-Augmented Generation (RAG) pipeline powered by Google's Flan-T5-XXL via HuggingFace Hub.

---

## Features

### Voice Assistant
- Time-aware greetings (morning / afternoon / evening)
- Continuous voice command loop with Google Speech Recognition
- Text-to-speech responses (pyttsx3 with configurable rate and voice)
- Wikipedia search and summarization
- Play YouTube videos by voice
- Google web search
- WhatsApp message automation
- Email sending via Gmail SMTP
- Real-time weather reports
- Top news headlines
- Trending movies list
- Random jokes and advice
- System IP address lookup
- Open local applications (Notepad, Calculator, CMD, Camera, Discord)

### Document Chat (Streamlit App)
- Multi-PDF upload and text extraction
- Chunked text processing with overlap (1 000 chars / 200 char overlap)
- Dense embeddings via `hkunlp/instructor-xl` (HuggingFace)
- FAISS vector store for sub-second semantic retrieval
- Conversational memory across turns (`ConversationBufferMemory`)
- Question answering powered by `google/flan-t5-xxl`

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Voice Assistant                      │
│                                                           │
│  Microphone → Google STT → Command Router → Action       │
│                                      │                    │
│                         ┌────────────┼────────────┐      │
│                     OS Ops    External APIs    pyttsx3    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                  Document Chat (Streamlit)                │
│                                                           │
│  PDFs → PyPDF2 → Text Chunks → Instructor-XL Embeddings  │
│                                          ↓                │
│  User Query → FAISS Retrieval → Flan-T5-XXL → Answer    │
│                        ↑                                  │
│              ConversationBufferMemory                     │
└─────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Voice Input | `SpeechRecognition` + Google Speech API |
| Voice Output | `pyttsx3` |
| Web UI | `Streamlit` |
| PDF Parsing | `PyPDF2` |
| Embeddings | `HuggingFaceInstructEmbeddings` (`hkunlp/instructor-xl`) |
| Vector Store | `FAISS` |
| LLM | `google/flan-t5-xxl` via HuggingFace Hub |
| LLM Orchestration | `LangChain` |
| Automation | `pywhatkit` (YouTube, WhatsApp, Google Search) |
| Configuration | `python-decouple` |
| HTTP Client | `requests` |

---

## Prerequisites

- Python **3.11**
- A working microphone (voice assistant mode)
- Pip or a virtual environment manager (venv / conda)
- API keys for all enabled services (see [Configuration](#configuration))
- `ffmpeg` or `portaudio` installed system-wide for audio support

### System-level audio (Linux / macOS)
```bash
# Ubuntu / Debian
sudo apt-get install portaudio19-dev python3-pyaudio

# macOS (Homebrew)
brew install portaudio
```

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/jarvis.git
cd jarvis

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install \
  pyttsx3 \
  SpeechRecognition \
  pywhatkit \
  wikipedia \
  requests \
  streamlit \
  langchain \
  huggingface_hub \
  InstructorEmbedding \
  faiss-cpu \
  PyPDF2 \
  python-decouple \
  numpy
```

> **Note:** For GPU-accelerated FAISS, replace `faiss-cpu` with `faiss-gpu`.

---

## Configuration

Copy the example environment file and fill in your credentials:

```bash
cp Jarvis/jarvis.env.example Jarvis/jarvis.env
```

Edit `Jarvis/jarvis.env`:

```ini
USER=YourName
BOTNAME=JARVIS

# News
NEWS_API_KEY=your_newsapi_key

# Weather
OPENWEATHER_APP_ID=your_openweathermap_key

# Movies
TMDB_API_KEY=your_tmdb_key

# HuggingFace (for document chat LLM)
HUGGINGFACEHUB_API_KEY=your_huggingface_key

# Gmail (for email sending)
EMAIL=your_gmail_address@gmail.com
PASSWORD=your_gmail_app_password
```

**Never commit your `.env` file.** Add it to `.gitignore`:

```
Jarvis/jarvis.env
```

### Obtaining API Keys

| Service | URL |
|---|---|
| NewsAPI | https://newsapi.org |
| OpenWeatherMap | https://openweathermap.org/api |
| TMDB | https://www.themoviedb.org/settings/api |
| HuggingFace | https://huggingface.co/settings/tokens |
| Gmail App Password | https://myaccount.google.com/apppasswords |

---

## Usage

### Voice Assistant

```bash
cd Jarvis
python jarvis.py
```

JARVIS will greet you and begin listening. Speak a command clearly into your microphone.

### Document Chat (Streamlit)

```bash
cd Jarvis
streamlit run main.py
```

Open `http://localhost:8501` in your browser:

1. Use the **sidebar** to upload one or more PDF files.
2. Click **Process** to index the documents.
3. Type questions in the main chat area and receive context-aware answers.

---

## Voice Commands

| Phrase | Action |
|---|---|
| `wikipedia <topic>` | Summarize a Wikipedia article |
| `play <song or video>` | Play on YouTube |
| `search for <query>` | Google search |
| `send whatsapp message` | Send a WhatsApp message |
| `send email` | Compose and send an email |
| `what's the weather` | Current weather for your location |
| `latest news` | Top news headlines |
| `trending movies` | Current TMDB trending movies |
| `tell me a joke` | Random joke |
| `give me advice` | Random advice |
| `what is my ip address` | Public IP lookup |
| `open notepad` | Launch Notepad |
| `open calculator` | Launch Calculator |
| `open command prompt` | Launch CMD |
| `open camera` | Launch camera app |
| `open discord` | Launch Discord |

---

## API Integrations

| Service | Purpose | Auth Required |
|---|---|---|
| Google Speech Recognition | Voice → text | No |
| NewsAPI | Headlines | Yes — `NEWS_API_KEY` |
| OpenWeatherMap | Weather | Yes — `OPENWEATHER_APP_ID` |
| TMDB | Trending movies | Yes — `TMDB_API_KEY` |
| HuggingFace Hub | LLM inference | Yes — `HUGGINGFACEHUB_API_KEY` |
| Wikipedia | Article summaries | No |
| YouTube (pywhatkit) | Video playback | No |
| Google Search (pywhatkit) | Web search | No |
| WhatsApp (pywhatkit) | Messaging | No |
| Gmail SMTP | Email | Yes — `EMAIL`, `PASSWORD` |
| Dad Joke API | Jokes | No |
| Advice Slip API | Advice | No |
| IPify | Public IP | No |

---

## Project Structure

```
VA-main/
├── Jarvis/
│   ├── functions/
│   │   └── os_ops.py          # OS-level operations (open apps, get IP)
│   ├── jarvis.py              # Core voice assistant engine
│   ├── main.py                # Streamlit document chat app
│   ├── utils.py               # Shared utility functions
│   └── jarvis.env             # Environment variables (do not commit)
└── README.md
```

---

## Known Limitations

- **Hardcoded paths:** `jarvis.py` contains an absolute path to the `.env` file. Update the `env_path` variable in [Jarvis/jarvis.py](Jarvis/jarvis.py) to match your local installation.
- **WhatsApp automation:** `pywhatkit` requires WhatsApp Web to be open in a browser and may break with WhatsApp Web updates.
- **Gmail SMTP:** Google requires an [App Password](https://myaccount.google.com/apppasswords) rather than your account password when 2FA is enabled.
- **Flan-T5-XXL inference:** Running this model via HuggingFace Hub requires a valid token with model access. Expect latency depending on Hub load.
- **Conversation memory:** Chat history is stored in-memory only and is lost when the Streamlit session ends.
- **Windows-only app paths:** OS application launch commands target Windows paths. Adjust `os_ops.py` for Linux/macOS.

---

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "feat: add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request.

Please follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines and include docstrings for any new functions.

---

## License

This project is licensed under the [MIT License](LICENSE).
