FROM python:3.10

WORKDIR /app

# Install ffmpeg (REQUIRED for Whisper)
RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]