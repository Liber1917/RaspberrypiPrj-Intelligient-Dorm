import time
import wave
import os
import json

from vosk import Model, KaldiRecognizer, SetLogLevel


def send_pipe(order_queue, action):
    if action == "-1":
        order_queue.put("voice_introduce")
    elif action == "0":
        order_queue.put("voice0")
        print("开灯")
    elif action == "1":
        order_queue.put("voice1")
        print("关灯")
    elif action == "2":
        order_queue.put("voice2")
        print("打开教务系统")
    elif action == "3":
        print("播报课表")
        order_queue.put("voice3")


def find_keyword(ret):
    with open("keyword_order.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
        for key, value in data.items():
            if key in ret:
                print(value)
                return value


def voice_recognization(order_queue):
    # You can set log level to -1 to disable debug messages
    str_ret = ''
    SetLogLevel(-1)
    print("开始加载模型")
    model = Model("../../model")

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
                        str_ret += result['text'] + ''

            result = json.loads(rec.FinalResult())
            if 'text' in result:
                str_ret += result['text']

            print(num, "  ", str_ret)
            wf.close()
            order = find_keyword(str_ret)
            send_pipe(order_queue, order)
            num += 1
        else:
            print("文件不存在")
            time.sleep(2)


if __name__ == '__main__':
    voice_recognization()
