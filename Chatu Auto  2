FROM python:3.10-slim

# FFmpeg इंस्टॉल करें (वीडियो-ऑडियो प्रोसेसिंग के लिए)
RUN apt-get update && apt-get install -y ffmpeg git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
