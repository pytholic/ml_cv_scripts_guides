import cv2

# Opens the Video file
cap= cv2.VideoCapture('./tello_data/videos/structure_1.mp4')
out_dir = './tello_data/frames/structure_1/'
idx=0
while(cap.isOpened()):
    ret, frame = cap.read()
    idx += 1
    if (idx % 1) == 0:
        if ret == False:
            break
        # flip for iphone
        #frame = cv2.flip(frame, -1)
        cv2.imwrite(out_dir + f'{idx:06d}.jpg', frame)


cap.release()
cv2.destroyAllWindows()