from io import BytesIO
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from llm_utils import api_call, api_call_function,system_prompt
from elevenlabs import  synthesize_speech
chat_history = [
    {"role": "system", "content": system_prompt}
]

class ChatInput(BaseModel):
    message: str

app = FastAPI()

# Allow frontend access (adjust origins if needed)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/chat")
async def chat_endpoint(payload: ChatInput):
    user_input = payload.message

    chat_history.append({"role": "user", "content": user_input})

    response = api_call(chat_history)
    message = response.choices[0].message

    if message.function_call:
        final_reply=  api_call_function(message,chat_history)
        chat_history.append({"role": "assistant", "content": final_reply})
        
        audio_bytes = synthesize_speech(final_reply)
        return StreamingResponse(BytesIO(audio_bytes), media_type="audio/mpeg")
    else:
        chat_history.append({"role": "assistant", "content": message.content})
        audio_bytes = synthesize_speech(message.content)
        return StreamingResponse(BytesIO(audio_bytes), media_type="audio/mpeg")

# For testing purpose of tts
@app.post("/speak")
async def speak(payload: dict):
    text = payload.get("text", "")
    audio_bytes = synthesize_speech(text)
    return StreamingResponse(BytesIO(audio_bytes), media_type="audio/mpeg")
