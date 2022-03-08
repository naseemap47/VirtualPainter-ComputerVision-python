import cv2
import os
import mediapipe as mp
import numpy as np

###############################
bresh_thickness = 5
eraser_thickness = 35
###############################

folder_path = 'Header Images'
img_list = os.listdir(folder_path)
img_list.sort()
# print(img_list)
over_lay = []
for img_path in img_list:
    image = cv2.imread(f'{folder_path}/{img_path}')
    over_lay.append(image)
# print(len(over_lay))

cap = cv2.VideoCapture(0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# print(width, height)

mp_hand = mp.solutions.hands
hand = mp_hand.Hands(max_num_hands=1,
                     min_detection_confidence=0.75,
                     min_tracking_confidence=0.25)
mp_draw = mp.solutions.drawing_utils

header = over_lay[0]
color = (255, 0, 255)
xp, yp = 0, 0
img_canvas = np.zeros((480, 640, 3), np.uint8)

while True:
    # 1. Import Image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # 2. Find Hand Landmarks
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hand.process(img_rgb)
    if result.multi_hand_landmarks:
        lm_list = []
        for hand_lm in result.multi_hand_landmarks:
            for id, lm in enumerate(hand_lm.landmark):
                img_height, img_width, channel = img.shape
                x, y = int(lm.x * img_width), int(lm.y * img_height)
                lm_list.append([id, x, y])
                # print(lm_list)
                # 3. Fingers Up or NOT
                if len(lm_list) > 20:
                    x1, y1 = lm_list[8][1:]
                    x2, y2 = lm_list[12][1:]

                    # 4. Index and middle finger Up - Selection Mode
                    if lm_list[8][2] < lm_list[6][2] and lm_list[12][2] < lm_list[10][2]:
                        # print('Index and Middle fingers are Up')
                        cv2.rectangle(img, (x1, y1-10), (x2, y2+10), color, cv2.FILLED)
                        if y1 < 70:
                            if 10 < x1 < 140:
                                header = over_lay[0]
                                color = (255, 0, 0)
                            elif 180 < x1 < 300:
                                header = over_lay[1]
                                color = (0, 0, 255)
                            elif 340 < x1 < 460:
                                header = over_lay[2]
                                color = (0, 255, 0)
                            elif 470 < x1 < 660:
                                header = over_lay[3]
                                color = (0, 0, 0)

                    # 5. If Index finger Up - Drawing Mode
                    elif lm_list[8][2] < lm_list[6][2]:
                        # print('Index finger is Up')
                        cv2.circle(img, (x1, y1), 8, color, cv2.FILLED)

                        if xp==0 and yp==0:
                            xp, yp = x1, y1
                        if color == (0, 0, 0):
                            cv2.line(img, (xp, yp), (x1, y1), color, eraser_thickness)
                            cv2.line(img_canvas, (xp, yp), (x1, y1), color, eraser_thickness)
                        else:
                            cv2.line(img, (xp, yp), (x1, y1), color, bresh_thickness)
                            cv2.line(img_canvas, (xp, yp), (x1, y1), color, bresh_thickness)
                        xp, yp = x1, y1

    # Setting Header Image
    img[0:70, 0:640] = header
    img = cv2.addWeighted(img, 0.5, img_canvas, 0.5, 0)
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", img_canvas)
    cv2.waitKey(1)
