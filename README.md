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
| LLM Backend      | `OpenAI GPT-4` with functions |
| Calendar API     | `Google Calendar API`         |
| Text-to-Speech   | `ElevenLabs TTS`             |
| Speech-to-Text   | `Chrome Web Speech API`       |
| Web Framework    | `FastAPI` (Python)           |
| Frontend         | `Vanilla JS + HTML/CSS`       |
| Env Management   | `python-dotenv`               |

---

## 🛠️ Project Structure

```
project/
│
├── main.py                     # FastAPI backend server
├── llm_utils.py                # OpenAI API + function calling
├── calendar_utils.py           # Google Calendar functions
├── elevenlabs_utils.py         # ElevenLabs STT + TTS helpers
├── templates/
│   └── index.html              # Frontend with Chrome STT
├── static/
│   └── style.css               # Optional styling
├── .env                        # Contains API keys (not committed)
└── README.md                   # This file
```

---

## 🔐 Environment Variables

Create a `.env` file in the root with the following:

```env
OPENAI_API_KEY=your_openai_key
ELEVEN_API_KEY=your_elevenlabs_key
VOICE_ID=your_elevenlabs_voice_id
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

---

## 🗣️ How It Works

1. User speaks to the browser using Chrome STT.
2. Transcription is sent to FastAPI backend.
3. OpenAI LLM interprets the query and calls appropriate calendar function.
4. The response is converted to voice using ElevenLabs TTS.
5. The TTS audio is streamed back and played in the browser.

---

## 📚 Supported Commands (Examples)

- “Schedule a meeting tomorrow at 3 PM for 30 minutes with Rohan.”
- “Cancel my meeting at 11 AM on Friday.”
- “What time am I free on 25th?”
- “List meetings after 2 PM today.”
- “Find 1 hour before my flight at 6 PM on Friday.”

---

## ✅ Future Improvements

- Memory with vector store (for “usual sync-ups”)
- User profile switching
- Slack/WhatsApp integrations
- Persistent context beyond one session

---

## 🧠 Credits

Built with ❤️ using:
- [OpenAI GPT-4](https://openai.com)
- [ElevenLabs TTS](https://elevenlabs.io)
- [Google Calendar API](https://developers.google.com/calendar)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Chrome Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)

---

## 📜 License

MIT License. Use and modify freely.