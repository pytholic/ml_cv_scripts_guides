import cv2

gopro = True

# Opens the Video file
cap = cv2.VideoCapture('/hdd/pytholic/droid_slam/data/gopro/input/videos/GH011823.MP4')
out_dir = '/hdd/pytholic/droid_slam/data/gopro/input/frames/GH011823/'

length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(length)
idx=0
while(cap.isOpened()):
    ret, frame = cap.read()
    idx += 1
    if (idx % 1) == 0:
        if ret == False:
            if gopro:
                continue
            else:
                break
        # for iphone
        #frame = cv2.flip(frame, -1)
        #frame = cv2.resize(frame, (1080, 1920))  # width, height
        
        # for evo
        frame = cv2.resize(frame, (1920, 1080))  # width, height
        
        cv2.imwrite(out_dir + f'{idx:06d}.jpg', frame)
        print(f"Frame {idx} done!")

    if idx == length:
        break

cap.release()
cv2.destroyAllWindows()
