import numpy as np
import wave
from scipy.io import wavfile
import matplotlib.pyplot as plt


def read_wav_data(filename):
    rate, data = wavfile.read(filename)
    data = data - np.mean(data)  # 消除直流分量
    data_out = data / np.max(np.abs(data))  # 幅值归一化
    return data_out


def wav_show(data, title='positive'):
    plt.plot(data)
    plt.title(title)
    plt.show()


if __name__ == '__main__':
    wav_show(read_wav_data('sound/1.wav'))