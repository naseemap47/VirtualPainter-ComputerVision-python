import cv2
import os

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
print(width, height)

while True:
    # 1. Import Image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # 2. Find Hand Landmarks
    
    # 3. Fingers Up or NOT
    # 4. Index and middle finger Up - Selection Mode
    # 5. If Index finger Up - Drawing Mode

    # Setting Header Image
    img[0:70, 0:640] = over_lay[0]

    cv2.imshow("Image", img)
    cv2.waitKey(1)
