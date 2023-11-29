# -*- coding: utf8 -*-
import cv2

# Step1：读取头像和国旗图像。
img_head = cv2.imread('head.jpg')
img_flag = cv2.imread('flag.jpg')

# Step2：把国旗叠加到头像上。
# Step2.1：获取头像和国旗宽度
w_head, h_head = img_head.shape[:2]
w_flag, h_flag = img_flag.shape[:2]
# Step2.2：根据宽度计算缩放比例
scale = w_head / w_flag / 4
# Step2.3：根据缩放比例缩放国旗
img_flag = cv2.resize(img_flag, (0, 0), fx=scale, fy=scale)
# Step2.4：获取缩放后国旗的新尺寸
w_flag, h_flag = img_flag.shape[:2]
# Step2.5：根据缩放后的尺寸叠加国旗到头像右下角
for c in range(0, 3):
    img_head[w_head - w_flag:, h_head - h_flag:, c] = img_flag[:, :, c]

# Step3：保存叠加后的图像
cv2.imwrite('new_head.jpg', img_head)
cv2.imshow("imshow",img_head)
cv2.waitKey(0)
cv2.destroyAllWindows()
