import subprocess
import argparse

parser = argparse.ArgumentParser(
                    prog = 'extract_frames',
                    description = 'frame extraction pipeline')

parser.add_argument('-d', '--device', help='capture device name', choices=['iphone', 'evo', 'gopro'], default='iphone')
parser.add_argument('-i', '--input', help='input file path')
parser.add_argument('-o', '--output', help='output path')
args = parser.parse_args()

if args.device == 'evo':
	size = '1920x1080'

output = args.output + '/%06d.jpg'

cmd = ['ffmpeg', 
           '-i', args.input, 
           '-s', size,
           '-pix_fmt', 'yuvj444p',
           output]

subprocess.run(cmd)
