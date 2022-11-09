import cv2
import os, glob
import argparse

parser = argparse.ArgumentParser(
                    prog = 'extract_frames',
                    description = 'frame extraction pipeline')

parser.add_argument('-c', '--cam', help='capture device name', choices=['iphone', 'evo', 'gopro'], default='iphone')
args = parser.parse_args()

# Opens the Video file
video_path = glob.glob('./tmp/*')
cap= cv2.VideoCapture(video_path[0])
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(length)

if not os.path.exists("./tmp/frames"):
    os.makedirs("./tmp/frames")

out_dir = './tmp/frames/'
idx=0

while(cap.isOpened()):
    ret, frame = cap.read()
    try:
        idx += 1
        if (idx % 1) == 0:
            # if ret == False:
            #     break
            # for iphone
            if args.cam == 'iphone':
                frame = cv2.flip(frame, -1)

            # for evo
            if args.cam == 'evo':
                frame = cv2.resize(frame, (1920, 1080))

            cv2.imwrite(out_dir + f'{idx:06d}.jpg', frame)
            print(f"Frame {idx} processed!")
    except:
        pass

cap.release()
cv2.destroyAllWindows()