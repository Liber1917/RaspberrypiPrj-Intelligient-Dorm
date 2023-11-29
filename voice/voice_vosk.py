import wave
import sys
import json

from vosk import Model, KaldiRecognizer, SetLogLevel

from record_10s import record_every_10s

# You can set log level to -1 to disable debug messages
SetLogLevel(-1)

num = input("录音编号")
record_every_10s(num)
wf = wave.open("sound/"+str(num)+".wav")

# model = Model(lang="en-us")
# You can also init model by name or with a folder path
# model = Model(model_name="vosk-model-en-us-0.21")
# 设置模型所在路径，刚刚4.1中解压出来的路径   《《《《
# model = Model("model")
model = Model("model-small")

rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)
# rec.SetPartialWords(True)   # 注释这行   《《《《

str_ret = ""

print("开始识别")
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = rec.Result()
        # print(result)

        result = json.loads(result)
        if 'text' in result:
            str_ret += result['text'] + ' '
    # else:
    #     print(rec.PartialResult())

# print(rec.FinalResult())
result = json.loads(rec.FinalResult())
if 'text' in result:
    str_ret += result['text']

print(str_ret)
