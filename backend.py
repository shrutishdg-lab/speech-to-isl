from fastapi import FastAPI, UploadFile, File
import whisper
import os

app = FastAPI()

model = None

@app.on_event("startup")
def load_model():
    global model
    model = whisper.load_model("base")

@app.post("/transcribe/")
async def transcribe(audio: UploadFile = File(...)):

    temp_file = "temp.wav"

    with open(temp_file, "wb") as f:
        f.write(await audio.read())

    result = model.transcribe(temp_file)
    text = result["text"]

    if os.path.exists(temp_file):
        os.remove(temp_file)
        
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend working"}