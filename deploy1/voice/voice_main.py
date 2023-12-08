import threading
from queue import Queue
from record_10s import record_every_10s
from voice_vosk import voice_recognization

order_queue = Queue()

thread = threading.Thread(target=record_every_10s)
thread2 = threading.Thread(target=voice_recognization, args=(order_queue,))

if __name__ == '__main__':
    # 启动线程
    thread.start()
    thread2.start()

    thread.join()
    thread2.join()