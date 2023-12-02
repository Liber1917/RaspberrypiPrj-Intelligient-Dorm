import whisper

model = whisper.load_model("base")
result = model.transcribe("/opt/000001.wav")
print(result["text"])