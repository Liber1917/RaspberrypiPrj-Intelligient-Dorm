import pyttsx3
import json


def listed():
    with open("keyword_order.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
        engine = pyttsx3.init()
        for key, value in data.items():
            engine.say(key+"命令码"+value)
            engine.runAndWait()


if __name__ == '__main__':
    listed()