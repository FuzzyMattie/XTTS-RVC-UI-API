import gradio as gr
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from threading import Thread
import uvicorn
from pathlib import Path
import time
from fastapi.middleware.cors import CORSMiddleware

import core_tts

app = FastAPI()

# Directory Setup
VOICE_DIR = Path("./voices")
RVC_DIR = Path("./rvcs")
SAMPLE_DIR = Path("./samples")

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

# Define FastAPI Endpoints
@app.get("/speakers_list")
async def speakers_list():
    rvc_models = [f.stem for f in RVC_DIR.glob("*.pth")]
    return JSONResponse(content=rvc_models)

@app.get("/speakers")
async def speakers():
    rvc_models = [f.stem for f in RVC_DIR.glob("*.pth")]
    speakers_data = [
        {
            "name": model_name,
            "voice_id": model_name,
            "preview_url": f"http://localhost:8000/sample/{model_name}.wav"
        }
        for model_name in rvc_models
    ]
    return JSONResponse(content=speakers_data)

@app.get("/languages")
async def get_languages():
    return JSONResponse(content={"languages": langs})

@app.get("/sample/{file_name}")
async def get_sample(file_name: str):
    file_path = SAMPLE_DIR / file_name
    if file_path.exists() and file_path.is_file():
        return FileResponse(path=file_path, media_type="audio/wav")
    return JSONResponse(status_code=404, content={"message": "File not found"})

@app.post("/set_tts_settings")
async def set_tts_settings(settings: dict):
    # Assume settings are applied successfully
    return JSONResponse(content={"message": "Settings successfully applied"})

@app.post("/tts_to_audio")
async def tts_to_audio(params_tts: dict):
    text = params_tts.get("text")
    text = str(text).replace('"',"").replace("*","")
    speaker_wav = params_tts.get("speaker_wav")
    language = params_tts.get("language")
    output_wav, rvc_output_wav = core_tts.runtts(
        rvc=speaker_wav+".pth",
        voice=speaker_wav+".wav",
        text=text,
        pitch_change=0,
        index_rate=0.75,
        language=language
    )
    return FileResponse(path=rvc_output_wav, media_type="audio/wav")

origins = [
    "http://localhost:8000",  # Add the origins that should be allowed to make requests
    "*",
    "https://lucky-lizards-dance.loca.lt/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
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
    core_tts.main()
    print("Starting api at http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
