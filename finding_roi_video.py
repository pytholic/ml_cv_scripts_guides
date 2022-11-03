import os, glob
import cv2
import numpy as np

video_path = '/home/pytholic/Desktop/Projects/icms_data/test_videos/new_car/0085.mp4'
#frame_number = 500
four_k = (3840, 2160)
FULL_HD = (1920,1080)
SD = (640, 480)

#cap = cv2.VideoCapture(video_path)
cap = cv2.VideoCapture(2)
#total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#print(width, height)

res = SD
cap.set(cv2.CAP_PROP_FRAME_WIDTH, res[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, res[1])
print(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# if frame_number >= 0 & frame_number <= total_frames:
#     cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

if (cap.isOpened()== False):
  print("Error opening video stream or file")

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:

        img = cv2.resize(frame, (640, 480))
        
        # For 4k
        # img_right = frame[int(round(0.4166*height, 0)):int(round(0.6944*height, 0)), int(round(0.8203*width, 0)):int(round(0.8984*width, 0))]
        # img_left = cv2.flip(frame, 1)
        # img_left = img_left[int(round(0.4166*height, 0)):int(round(0.6944*height, 0)), int(round(0.7682*width, 0)):int(round(0.8463*width, 0))]
        # img_left = cv2.flip(img_left, 1)
        
        # img_right = frame[900:1500, 3150:3450]
        # img_left = cv2.flip(frame, 1)
        # img_left = img_left[900:1500, 2950:3250]
        # img_left = cv2.flip(img_left, 1)

        # img_right = frame[700:1500, 3000:3400]
        # img_left = cv2.flip(frame, 1)
        # img_left = img_left[700:1500, 3000:3400]
        # img_left = cv2.flip(img_left, 1)


        # For Full HD
        # img_right = img[300:900, 1450:1700]
        # img_left = cv2.flip(img, 1)
        # img_left = img_left[300:900, 1450:1700]
        # img_left = cv2.flip(img_left, 1)
        # img_right = frame[300:900, 1450:1700]
        # img_left = cv2.flip(frame, 1)
        # img_left = img_left[300:900, 1450:1700]
        # img_left = cv2.flip(img_left, 1)

        # For SD
        # Normal case
        img_right = img[50:450, 0:100]
        img_left = cv2.flip(img, 1)
        img_left = img_left[50:450, 0:100]
        img_left = cv2.flip(img_left, 1)

        # Resized case from full HD
        # img_right = img[50:450, 50:150]
        # img_left = cv2.flip(img, 1)
        # img_left = img_left[50:450, 40:140]
        # img_left = cv2.flip(img_left, 1)


        # #horizontal_stack = np.hstack((img_left, img_right))
        horizontal = np.concatenate((img_left, img_right), axis=1)

        cv2.namedWindow("output", cv2.WINDOW_NORMAL)
        cv2.imshow('output', horizontal)

        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
