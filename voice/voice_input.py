import pyaudio
import numpy as np
import wave


def monitor_mic(th, filename):
    print("start recording")
    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000  # 录音时的采样率
    WAVE_OUTPUT_FILENAME = filename + ".wav"
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    while True:
        for i in range(0, 5):
            data = stream.read(CHUNK)
            frames.append(data)
        audio_data = np.frombuffer(data, dtype=np.short)
        temp = np.max(audio_data)
        if temp > th:
            frames2 = []
            print("detected a signal")
            print('current threshold：', temp)
            # 这里只录制30个CHUNK
            print("recording")
            for i in range(0, 30):
                data2 = stream.read(CHUNK)
                frames2.append(data2)
            stream.stop_stream()
            stream.close()
            p.terminate()
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames2))
            wf.close()
            break


if __name__ == '__main__':
    while True:
        num = input("filename:")
        if num == "exit":
            break
        monitor_mic(1000, "sound/"+num)