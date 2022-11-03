import os, glob
import cv2
import numpy as np

video_path = '/home/pytholic/Desktop/Projects/icms_data/test_videos/new_car/test.mp4'
frame_number = 500

cap = cv2.VideoCapture(video_path)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

def adjust_gamma(image, gamma=2.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)

if frame_number >= 0 & frame_number <= total_frames:
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

if (cap.isOpened()== False):
  print("Error opening video stream or file")

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:

        #print(frame.shape)
        frame = cv2.resize(frame, (1920, 1080))
        frame = adjust_gamma(frame)
        # img_right = frame[400:700, 1450:1700]
        # img_left = cv2.flip(frame, 1)
        # img_left = img_left[400:700, 1450:1700]
        # img_left = cv2.flip(img_left, 1)

        # # #horizontal_stack = np.hstack((img_left, img_right))
        # horizontal = np.concatenate((img_left, img_right), axis=1)

        cv2.namedWindow("output", cv2.WINDOW_NORMAL)
        cv2.imshow('output', frame)

        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
    else:
        break

cap.realease()
cap.destroyAllWindows()
