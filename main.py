
from elevenlabs_tts import  synthesize_speech
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm_utils import api_call, api_call_function, system_prompt

chat_history = [{"role": "system", "content": system_prompt}]


class ChatInput(BaseModel):
    message: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)


def text_to_audio_stream(chat_history):
    fn_name        = None
    fn_args_raw    = ""       # JSON comes in fragments!
    buf = ""
    buf2 = ""
    for chunk in api_call(chat_history):
        delta = chunk.choices[0].delta
   
        if delta.function_call:
            print("delta")
            print(delta.function_call)
            if delta.function_call.name:
                print("fucntion")
                fn_name = delta.function_call.name      # appears once
            if delta.function_call.arguments:
                print("arguments")
                fn_args_raw += delta.function_call.arguments  # append args
                print(fn_args_raw)
        else:
            buf += delta.content or ""
            #  punctuation or ≥120 chars
            if any(buf.endswith(p) for p in ".!?") or len(buf) >= 120:
                yield from synthesize_speech(buf)               # TTS
                buf = ""

    if buf:                                          # tail 
        yield from synthesize_speech(buf)
    else:
        for chunks in api_call_function(fn_name,fn_args_raw,chat_history):
            delta2 = chunks.choices[0].delta
            buf2 += delta2.content or ""
            #  punctuation or ≥120 chars
            if any(buf2.endswith(p) for p in ".!?") or len(buf2) >= 120:
                yield from synthesize_speech(buf2)               # TTS
                buf2 = ""
        if buf2:                                          # tail
            yield from synthesize_speech(buf2)


@app.post("/chat")
async def chat_endpoint(payload: ChatInput):
    chat_history.append({"role": "user", "content": payload.message})
    return StreamingResponse(text_to_audio_stream(chat_history),media_type="audio/mpeg")

# main.py  (run with:  uvicorn main:app --reload)
