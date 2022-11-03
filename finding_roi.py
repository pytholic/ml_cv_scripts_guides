import os, glob
import cv2
import numpy as np

in_dir = '/home/pytholic/Desktop/Projects/datasets/window_detection/data/frames/0015'

for image in glob.glob(in_dir + '/*.jpg'):
    """
    Image size: (1080, 1920)
    Right crop: img[300:900, 1450:1700]
    """
    name = image.split('/')[-1]
    img = cv2.imread(image)
    
    # for tinted
    #img = img[232:285, 580:690]  # 037
    #img = img[259:293, 1316:1377]  # 037
    #img = img[163:243, 1292:1381]  # 051
    #img = img[162:197, 595:631]  # 051
    
    # for not tinted
    # For HD
    # img_right = img[300:900, 1450:1700]
    # img_left = cv2.flip(img, 1)
    # img_left = img_left[300:900, 1450:1700]
    # img_left = cv2.flip(img_left, 1)
    # img_right_back = img[222:265, 1200:1250]

    # For 4k
    img_right = img[900:1500, 3150:3450]
    img_left = cv2.flip(img, 1)
    img_left = img_left[900:1500, 2950:3250]
    img_left = cv2.flip(img_left, 1)

    horizontal = np.concatenate((img_left, img_right), axis=1)

    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    cv2.imshow('output', horizontal)   
    if cv2.waitKey(0) & 0xFF == 27:
            break

cv2.destroyAllWindows()