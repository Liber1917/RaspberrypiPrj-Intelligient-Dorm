import snowboydecoder_2
import wave
import pyaudio
import signal

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


def play_wav_file(filename):
    wav_file = wave.open(filename, 'rb')
    audio_stream = pyaudio.PyAudio().open(format=pyaudio.get_format_from_width(wav_file.getsampwidth()),
                                          channels=wav_file.getnchannels(),
                                          rate=wav_file.getframerate(),
                                          output=True)
    chunk_size = 1024
    data = wav_file.readframes(chunk_size)
    while data:
        audio_stream.write(data)
        data = wav_file.readframes(chunk_size)
    audio_stream.stop_stream()
    audio_stream.close()
    wav_file.close()


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
if right:
    play_wav_file('../科莱让你别卷了.wav')

detector.terminate()
