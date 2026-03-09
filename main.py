from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os
import uuid

from whisper_engine import transcribe_audio
from isl_engine import convert_to_isl

app = FastAPI()

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -------- Root endpoint --------
@app.get("/")
def root():
    return {"message": "Speech to ISL backend running"}


# -------- Text request model --------
class TextRequest(BaseModel):
    text: str


# -------- Realtime text endpoint --------
@app.post("/realtime/")
async def realtime_translate(request: TextRequest):
    try:
        text = request.text
        isl_text = convert_to_isl(text)

        return {
            "input_text": text,
            "isl_gloss": isl_text
        }

    except Exception as e:
        return {"error": str(e)}


# -------- Audio endpoint --------
@app.post("/translate/")
async def translate(audio: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.wav")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        # speech → text using Whisper
        text = transcribe_audio(file_path)

        # text → ISL
        isl_text = convert_to_isl(text)

        os.remove(file_path)

        return {
            "speech_text": text,
            "isl_gloss": isl_text
        }

    except Exception as e:
        return {"error": str(e)}