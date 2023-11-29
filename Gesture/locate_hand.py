import cv2
import mediapipe as mp
import time
import numpy as np



def locate_hand():
    print("project start")
    cap = cv2.VideoCapture(1)
    model_list = list()  # 数据集处理

    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    pTime = 0
    cTime = 0

    points = np.array(object=tuple)

    if cap.isOpened():
        print("camera opened")
        # np.delete(points, 0, axis=0)
        while True:
            success, img = cap.read()
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 2 = to
            results = hands.process(imgRGB)
            # print(results.multi_hand_landmarks)//检查手坐标输出
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    for id, lm in enumerate(handLms.landmark):
                        # print(id, lm)
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        point = (cx, cy)
                        # point_dic[id] = point
                        np.append(point, points)
                        # print(id, cx, cy)
                        cv2.putText(img, str(id), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)

                        # if id == 4:
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 255, 255), 2)

            cv2.imshow("Image", img)
            order = cv2.waitKey(1)

            if order == 113:
                print("quit")
                return model_list
            elif order != -1:
                print("order", int(order)-48)
                sample = landmarks_to_numpy(results)
                model_list.append([int(order)-48, sample])
                print("save the points")
    else:
        print("no camera")
        return 0


def landmarks_to_numpy(results):
    """
    将landmarks格式的数据转换为numpy格式的数据
    numpy shape:(2, 21, 3)
    :param results:
    :return:
    """
    shape = (2, 21, 3)
    landmarks = results.multi_hand_landmarks
    if landmarks is None:
        # 没有检测到手
        return np.zeros(shape)
    elif len(landmarks) == 1:
        # 检测出一只手，先判断是左手还是右手
        label = results.multi_handedness[0].classification[0].label
        hand = landmarks[0]
        # print(label)
        if label == "Left":
            return np.array(
                [np.array([[hand.landmark[i].x, hand.landmark[i].y, hand.landmark[i].z] for i in range(21)]),
                 np.zeros((21, 3))])
        else:
            return np.array([np.zeros((21, 3)),
                             np.array(
                                 [[hand.landmark[i].x, hand.landmark[i].y, hand.landmark[i].z] for i in range(21)])])
    elif len(landmarks) == 2:
        # print(results.multi_handedness)
        lh_idx = 0
        rh_idx = 0
        for idx, hand_type in enumerate(results.multi_handedness):
            label = hand_type.classification[0].label
            if label == 'Left':
                lh_idx = idx
            if label == 'Right':
                rh_idx = idx

        lh = np.array(
            [[landmarks[lh_idx].landmark[i].x, landmarks[lh_idx].landmark[i].y, landmarks[lh_idx].landmark[i].z] for i
             in range(21)])
        rh = np.array(
            [[landmarks[rh_idx].landmark[i].x, landmarks[rh_idx].landmark[i].y, landmarks[rh_idx].landmark[i].z] for i
             in range(21)])
        return np.array([lh, rh])
    else:
        return np.zeros((2, 21, 3))


def standardization(hand_arr):
    """
    均值方差归一化
    :param hand_arr:numpy数组
    :return:
    """
    return (hand_arr - np.mean(hand_arr)) / np.std(hand_arr)


def relative_coordinate(arr, point):
    """
    转化为相对坐标
    :param arr: numpy数组
    :param point: 手掌根部坐标点
    :return:
    """
    return arr - point


def process_mark_data(hand_arr):
    """
    处理手部坐标点信息数组
    将所有点处理为相对于手掌根部点的相对位置
    :param hand_arr: 手部numpy数组
    :return:
    """
    lh_root = hand_arr[0, 0]
    rh_root = hand_arr[1, 0]
    lh_marks = relative_coordinate(hand_arr[0, 1:], lh_root)
    rh_marks = relative_coordinate(hand_arr[1, 1:], lh_root)
    if lh_marks.all() != 0:
        lh_marks = standardization(lh_marks)
    if rh_marks.all() != 0:
        rh_marks = standardization(rh_marks)
    return np.array([lh_marks, rh_marks])
