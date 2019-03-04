import cv2
import numpy as np

imgs = cv2.imread("./imgs/gakki.png",cv2.COLOR_BGR2RGB)
img2 = cv2.rectangle(imgs,(0,0),(40,40),(0,255,0),4)

cv2.imshow("hello",img2)
cv2.waitKey()
cv2.destroyWindow()