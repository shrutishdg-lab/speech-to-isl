import sounddevice as sd
import numpy as np
import queue
import threading
from faster_whisper import WhisperModel

# ================= SETTINGS =================
samplerate = 16000
block_duration = 0.5
chunk_duration = 2.0
channels = 1

frames_per_block = int(samplerate * block_duration)
frames_per_chunk = int(samplerate * chunk_duration)

audio_queue = queue.Queue()

# ================= MODEL =================
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

# ================= AUDIO CALLBACK =================
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())

# ================= RECORDER =================
def recorder():
    with sd.InputStream(
        samplerate=samplerate,
        channels=channels,
        blocksize=frames_per_block,
        callback=audio_callback
    ):
        print("🎤 Listening... Speak now (Ctrl+C to stop)")
        sd.sleep(10000)  # 10 seconds


# ================= TRANSCRIBER =================
def transcriber():
    buffer = []
    last_text = ""   # Prevent repeated retrieval spam

    while True:
        block = audio_queue.get()
        buffer.append(block)

        total_frames = sum(len(b) for b in buffer)

        if total_frames >= frames_per_chunk:
            audio = np.concatenate(buffer, axis=0)
            audio = audio[:, 0].astype(np.float32)
            audio /= np.max(np.abs(audio)) + 1e-9
            buffer = []

            segments, _ = model.transcribe(
                audio,
                language="en",
                task="transcribe",
                beam_size=5,
                best_of=5,
                vad_filter=True,
                vad_parameters=dict(
                    min_silence_duration_ms=300
                )
            )

            for segment in segments:
                text = segment.text.strip()

                if text and text != last_text:
                    last_text = text

                    print("\n📝 User said:", text)

                   

# ================= MAIN =================
if __name__ == "__main__":
    try:
        threading.Thread(target=recorder, daemon=True).start()
        transcriber()
    except KeyboardInterrupt:
        print("\n🛑 Stopping transcription. Goodbye!")
