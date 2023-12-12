import threading
from queue import Queue
from voice.record_10s import record_every_10s
from voice.voice_vosk import voice_recognization
from order_request.order_request import order_react
# from snowboy import snowboydecoder_2
from Gesture import Test_recognize
import signal

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


order_queue = Queue()

thread = threading.Thread(target=record_every_10s)
thread2 = threading.Thread(target=voice_recognization, args=(order_queue,))
thread3 = threading.Thread(target=order_react, args=(order_queue,))
thread4 = threading.Thread(target=Test_recognize.get_gesture, args=(order_queue,))

if __name__ == '__main__':
    # model = "../snowboy/wake_up.pmdl"

    # # capture SIGINT signal, e.g., Ctrl+C
    # signal.signal(signal.SIGINT, signal_handler)

    # detector = snowboydecoder_2.HotwordDetector(model, sensitivity=0.5)
    # print('Listening... Press Ctrl+C to exit')

    # right = detector.start(detected_callback=snowboydecoder_2.play_audio_file(),
    #                        interrupt_check=interrupt_callback,
    #                        sleep_time=0.03)
    # print(right)

    # detector.terminate()
    # 启动线程
    right = True
    if right:
        print("start")
        thread.start()
        thread2.start()
        thread3.start()
        #thread4.start()

        thread.join()
        thread2.join()
        thread3.join()
        #thread4.join()
