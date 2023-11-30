import wave
import os
import json

from vosk import Model, KaldiRecognizer, SetLogLevel


def voice_recognization():
    # You can set log level to -1 to disable debug messages
    str_ret = ''
    SetLogLevel(-1)
    model = Model("model-small")

    num = 0
    while True:
        if os.path.exists("sound/" + str(num) + ".wav"):
            wf = wave.open("sound/" + str(num) + ".wav")
            rec = KaldiRecognizer(model, wf.getframerate())
            rec.SetWords(True)
            str_ret = ""
            print("开始识别")
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = rec.Result()

                    result = json.loads(result)
                    if 'text' in result:
                        str_ret += result['text'] + ' '

            result = json.loads(rec.FinalResult())
            if 'text' in result:
                str_ret += result['text']

            print(num, "  ", str_ret)
            wf.close()
            find_keyword(str_ret)
            num += 1
        else:
            print("文件不存在")


def find_keyword(ret):
    with open("keyword_order.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
        for key, value in data.items():
            if key in ret:
                print(value)
                return value


if __name__ == '__main__':
    voice_recognization()
