# import requests
import os
from elevenlabs.client import ElevenLabs

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

VOICE_ID  = "JBFqnCBsd6RMkjVDRZzb"                 
MODEL_ID  = "eleven_multilingual_v2"
client    = ElevenLabs(api_key = ELEVEN_API_KEY)                             

def synthesize_speech(text: str):
    audio_gen = client.text_to_speech.stream(
        text=text,
        voice_id=VOICE_ID,
        model_id=MODEL_ID
    )                                                
    for chunk in audio_gen:                          
        if isinstance(chunk, bytes):
            yield chunk

