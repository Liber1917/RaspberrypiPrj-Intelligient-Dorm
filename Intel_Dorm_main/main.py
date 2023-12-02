import threading
from queue import Queue
from voice.record_10s import record_every_10s
from voice.voice_vosk import voice_recognization
from order_request.order_request import order_react

order_queue = Queue()

thread = threading.Thread(target=record_every_10s)
thread2 = threading.Thread(target=voice_recognization, args=(order_queue,))
thread3 = threading.Thread(target=order_react, args=(order_queue,))

if __name__ == '__main__':
    # 启动线程
    thread.start()
    thread2.start()
    thread3.start()

    thread.join()
    thread2.join()
    thread3.join()