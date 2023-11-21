import numpy as np
import pandas as pd
import re


def str2list(string: str):
    """
    统一坐标系：以[0]为原点
    :param string:
    :return:
    """
    x = re.split(r'[, ]', string[1:-1])
    print(x)
    point_x = int(x[0])
    point_y = int(x[-1])
    return [point_x, point_y]


def csv2numpy_for_tensorflow(file, label):
    """
    :param file:
    :param label:
    size:int+int  e.g.12
    1 -> left
    2->right

    1 -> 食指
    ...
    :return:
    """
    px = file1.iat[0, 0]
    print(px, "  ", type(px))
    print(str2list(px), type(str2list(px)))
    px = str2list(px)
    sample = list()
    for index, row in file.iterrows():
        Row = list()
        for value in row:
            v = str2list(value)
            print(value, type(value))
            Row.append(np.array([v[0] - px[0], v[1] - px[1], label]))
        print(Row)
        sample.append(Row)


file1 = pd.read_csv("hand_data_1.csv")
csv2numpy_for_tensorflow(file1, 12)
