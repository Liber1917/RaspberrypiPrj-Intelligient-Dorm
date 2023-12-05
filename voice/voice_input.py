import wave
import pyttsx3


def save_as_wav(text, output_file):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_file)
    engine.runAndWait()


# 示例文本和输出文件路径
text = "我在"
output_file = "../sound/0.wav"

# 将文本保存为 .wav 文件
save_as_wav(text, output_file)