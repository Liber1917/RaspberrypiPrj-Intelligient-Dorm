import threading
import locate_hand as lh
import cv2

thread1 = threading.Thread(name='locate_hand', target=lh.locate_hand)
thread1.start()
