import requests
import os
from dotenv import load_dotenv
load_dotenv()  

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

if not ELEVEN_API_KEY:
    raise ValueError("Please set the ELEVEN_API_KEY environment variable.")

def synthesize_speech(text):
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        headers={
            "xi-api-key": ELEVEN_API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "text": text,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},"speed": "1.3"
        }
    )
    return response.content
