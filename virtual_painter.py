import cv2
import os

folder_path = 'Header Images'
img_list = os.listdir(folder_path)
img_list.sort()
print(img_list)

cap = cv2.VideoCapture(0)
cap.set(3, 1020)
cap.set(4, 720)

while True:
    success, img = cap.read()

    cv2.imshow("Image", img)
    cv2.waitKey(1)