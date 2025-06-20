# 🧠 Smart Scheduler Voice Assistant

Smart Scheduler is a conversational AI agent that helps users manage their Google Calendar using **voice interaction**. It supports scheduling, checking, listing, and canceling meetings using natural conversation powered by OpenAI's function calling, ElevenLabs TTS, and Chrome's built-in STT.

---

## ✨ Features

- ✅ **Voice input** using Chrome Speech-to-Text
- ✅ **Natural conversation** powered by OpenAI's LLM with function calling
- ✅ **Real-time Google Calendar integration**
- ✅ **ElevenLabs TTS** for clear voice responses
- ✅ Handles vague, contextual, and relative time requests
- ✅ Reacts with short, crisp replies for fast TTS interaction

---

## ⚙️ Tech Stack

| Layer            | Tool / API Used              |
|------------------|------------------------------|
| LLM Backend      | `OpenAI GPT-40-mini` with functions |
| Calendar API     | `Google Calendar API`         |
| Text-to-Speech   | `ElevenLabs TTS`             |
| Speech-to-Text   | `Chrome Web Speech API`       |
| Web Framework    | `FastAPI` (Python)           |
| Frontend         | `Vanilla JS + HTML/CSS`       |
| Env Management   | `python-dotenv`               |

---

## 🔐 Environment Variables

Create a `.env` file in the root with the following:

```env
OPENAI_API_KEY=your_openai_key
ELEVEN_API_KEY=your_elevenlabs_key
```

---

## 🚀 How to Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/your-username/smart-scheduler.git
cd smart-scheduler
```

### 2. Set up Python environment

```bash
pip install -r requirements.txt
```

### 3. Add `.env` file with your API keys

As shown above.

### 4. Authenticate Google Calendar API

- Enable **Google Calendar API** at [Google Cloud Console](https://console.cloud.google.com/).
- Download `credentials.json` and place it in the root.
- On first run, it will prompt a browser-based OAuth login.

### 5. Run the FastAPI server

```bash
uvicorn main:app --reload
```

### 6. Open `index.html` in browser (Chrome only)

```bash
http://127.0.0.1:5500/index.html
```
