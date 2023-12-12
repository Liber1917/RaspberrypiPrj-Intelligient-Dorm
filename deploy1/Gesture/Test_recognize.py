try:
    import tensorflow as tf
    import cv2
except ImportError:
    print("lack cv2 or tensorflow")
try:
    import mediapipe as mp
    import time
    import numpy as np
    from queue import Queue
except ImportError:
    print("lack mediapipe or numpy")
from locate_hand import landmarks_to_numpy
from locate_hand import process_mark_data


def get_gesture(order_queue):
    loaded_model = tf.saved_model.load('model/src')

    print("start")
    cap = cv2.VideoCapture(0)
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
                        # print(id, cx, cy)
                        cv2.putText(img, str(id), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)

                        # if id == 4:
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            predicted_label = 0
            if results.multi_hand_landmarks:
                sample = landmarks_to_numpy(results)
                sample = process_mark_data(sample)
                mid = [sample]
                sample = np.array(mid)
                print("sample", sample)
                input_1 = tf.constant(sample, dtype=tf.float32, name='dense_input')
                out_data = loaded_model(input_1)
                predicted_label = tf.argmax(out_data, axis=1).numpy()
                print(out_data)
                order_queue.put(int(predicted_label[0]))
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(img, str(predicted_label), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 255, 255), 2)

            cv2.imshow("Image", img)
            order = cv2.waitKey(1)
            # print(order)


    else:
        print("no camera")
        
        
if __name__ == "__main__":
	print("sss")
	order = Queue()
	get_gesture(order)
	
