from fastapi import FastAPI, UploadFile, File
import shutil
import os

from whisper_engine import transcribe_audio
from isl_engine import convert_to_isl

app = FastAPI()

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"status": "Speech to ISL backend running"}

@app.post("/translate/")
async def translate(audio: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, audio.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    text = transcribe_audio(file_path)

    isl_text = convert_to_isl(text)

    return {
        "speech_text": text,
        "isl_gloss": isl_text
    }