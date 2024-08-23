import gradio as gr
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from threading import Thread
import uvicorn
from pathlib import Path
import time
from fastapi.middleware.cors import CORSMiddleware
import json

import core_tts

app = FastAPI()

# Directory Setup
VOICE_DIR = Path("./voices")
RVC_DIR = Path("./rvcs")
CONFIG_FILE = "voice_models.json"

# Load configurations from the JSON file
def load_voice_models():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {}

# Language Mapping
langs = {
    "Arabic": "ar",
    "Brazilian Portuguese": "pt",
    "Chinese": "zh-cn",
    "Czech": "cs",
    "Dutch": "nl",
    "English": "en",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Polish": "pl",
    "Russian": "ru",
    "Spanish": "es",
    "Turkish": "tr",
    "Japanese": "ja",
    "Korean": "ko",
    "Hungarian": "hu",
    "Hindi": "hi"
}
@app.options("/speakers_list")
@app.options("/speakers")
@app.options("/languages")
@app.options("/sample/{file_name}")
@app.options("/set_tts_settings")
@app.options("/tts_to_audio")


@app.get("/speakers_list")
async def speakers_list():
    # Return a list of speaker names from the voice models configuration
    speaker_names = list(voice_models.keys())
    return JSONResponse(content=speaker_names)

@app.get("/speakers")
async def speakers():
    speakers_data = [
        {
            "name": name,
            "voice_id": name,
            "preview_url": f"http://localhost:8000/sample/{voice_model['reference_voice']}"
        }
        for name, voice_model in voice_models.items()
    ]
    return JSONResponse(content=speakers_data)

@app.get("/languages")
async def get_languages():
    return JSONResponse(content={"languages": langs})

@app.get("/sample/{file_name}")
async def get_sample(file_name: str):
    file_path = VOICE_DIR / file_name
    if file_path.exists() and file_path.is_file():
        return FileResponse(path=file_path, media_type="audio/wav")
    return JSONResponse(status_code=404, content={"message": "File not found"})

@app.post("/set_tts_settings")
async def set_tts_settings(settings: dict):
    return JSONResponse(content={"message": "Settings successfully applied"})

@app.post("/tts_to_audio")
async def tts_to_audio(params_tts: dict):
    print(params_tts)
    text = params_tts.get("text")
    text = str(text).replace('"',"").replace("*","")
    speaker_wav = params_tts.get("speaker_wav")
    voice_model = voice_models.get(speaker_wav)
    try:
        output_wav, rvc_output_wav = core_tts.runtts(
            voice_model=str(voice_model).replace("'",'"'),
            text=text,
            pitch_change=0,
            index_rate=0.75
        )
        return FileResponse(path=rvc_output_wav, media_type="audio/wav")
    except:
        return JSONResponse(content={"message": "TTS has failed"})

origins = [
    "http://localhost:8000",  
    "*",
    "https://lucky-lizards-dance.loca.lt/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http':
            request = Request(scope, receive)
            start_time = time.time()
            logger.info(f"Request: {request.method} {request.url}")
            print(f"Request: {request.method} {request.url}")
            body = await request.body()
            logger.info(f"Body: {body.decode('utf-8')}")

            async def custom_send(message):
                if message['type'] == 'http.response.body':
                    duration = time.time() - start_time
                    logger.info(f"Duration: {duration:.2f} seconds")
                await send(message)

            await self.app(scope, receive, custom_send)


def startAPI():
    global voice_models
    voice_models = load_voice_models()
    core_tts.main()
    print("Starting api at http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
