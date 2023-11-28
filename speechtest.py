#import pyttsx3 as pyttsx
import speech_recognition as sr

# 创建语音识别器对象
r = sr.Recognizer()

# 音频文件路径
wav_file = "科莱让你别卷了.wav"

# 使用 AudioFile 打开音频文件
with sr.AudioFile(wav_file) as source:
    # 读取音频文件数据
    print("正在分析音频文件数据...")
    audio = r.record(source)
    print("开始识别")
    # 进行语音识别
    try:
        text = r.recognize_google(audio, language='zh-CN')
        print('识别结果：', text)
    except sr.UnknownValueError:
        print('无法识别语音')
    except sr.RequestError as e:
        print('请求错误：', str(e))
