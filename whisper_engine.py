import whisper

model = None


def load_model():
    global model

    if model is None:
        try:
            print("Loading Whisper model (tiny)...")
            model = whisper.load_model("tiny")  # best for small servers
            print("Whisper model loaded successfully.")
        except Exception as e:
            print("Error loading Whisper model:", str(e))
            raise RuntimeError("Failed to load Whisper model")

    return model


def transcribe_audio(audio_path: str) -> str:
    try:
        model_instance = load_model()

        print(f"Transcribing audio: {audio_path}")

        result = model_instance.transcribe(audio_path)

        text = result.get("text", "").strip()

        print("Transcription result:", text)

        return text

    except Exception as e:
        print("Transcription error:", str(e))
        return "Transcription failed"