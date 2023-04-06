import subprocess
import argparse
import os, glob

parser = argparse.ArgumentParser(
                    prog='extract_frames',
                    description='frame extraction pipeline')

parser.add_argument('-d', '--device', help='capture device name',
                    choices=['iphone', 'evo', 'gopro'], default='gopro')
args = parser.parse_args()

video_path = glob.glob('./tmp/*')

if not os.path.exists("./tmp/frames"):
    os.makedirs("./tmp/frames")

out_dir = './tmp/frames/'
output = out_dir + '%06d.jpg'

if args.device == 'evo':
    size = '1920x1080'
    cmd = ['ffmpeg', '-i', video_path[0], '-s', size, output]
else:
    cmd = ['ffmpeg', '-i', video_path[0], output]

subprocess.run(cmd)
