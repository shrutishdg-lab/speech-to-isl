import whisper

model = None

def load_model():
    global model
    if model is None:
        print("Loading Whisper model...")
        model = whisper.load_model("tiny")   # tiny model works best for small servers
    return model


def transcribe_audio(audio_path):
    model_instance = load_model()
    result = model_instance.transcribe(audio_path)
    return result["text"]