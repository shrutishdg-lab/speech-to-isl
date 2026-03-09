from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
import base64
import uuid

from whisper_engine import transcribe_audio
from isl_engine import convert_to_isl

app = FastAPI()

# -------- CORS FIX --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)