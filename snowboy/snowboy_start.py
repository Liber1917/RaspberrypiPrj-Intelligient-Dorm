import snowboydecoder_2
import sys
import signal

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


model = "../snowboy/wake_up.pmdl"

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder_2.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

# main loop
right = detector.start(detected_callback=snowboydecoder_2.play_audio_file(),
               interrupt_check=interrupt_callback,
               sleep_time=0.03)
print(right)

detector.terminate()
