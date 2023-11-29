# 周日-72
# 周一-0
# 周二-12
# 周三-24
# 周四-36
# 周五-48
# 周六-60

import pyttsx3

# 创建 TTS 引擎实例
engine = pyttsx3.init()

# 设置语速（可选）
engine.setProperty('rate', 150)  # 设置语速为 150 字符/分钟

# 设置音量（可选）
engine.setProperty('volume', 0.8)  # 设置音量为 0.8

# 要转换的文本
text = "Hello, how are you today?"

# 将文本转换为语音
engine.say(text)

# 播放语音
engine.runAndWait()