import time
import pyaudio
import wave
import subprocess


def record_every_10s():
    """
    每5秒录音一次
    :return:
    """
    name = 0
    while True:
        path = "voice/sound/"+str(name)+".wav"

        print("开始录音,请说话......")
        subprocess.run(["touch", path])
        command = ['arecord', '-D', 'hw:2,0', '-f', 'S16_LE', '-r', '44100', '-c', '1', '-d', '5', '-t', 'wav', path]
        subprocess.run(command)
        name+=1


if __name__ == '__main__':
    record_every_10s()

    


