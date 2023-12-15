import wave
import pyttsx3


def save_as_wav():
    engine = pyttsx3.init()
    engine.setProperty("volume", 1.0)
    engine.setProperty("voice", 'zh')
    engine.say("今天没有课")
    engine.runAndWait()


# 示例文本和输出文件路径
text = "我在"
output_file = "../sound/0.wav"

# 将文本保存为 .wav 文件
save_as_wav()
