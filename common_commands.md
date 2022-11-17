```sh
# Extract frames with size and rotation
# rotation = PI, PI/2 etc.
ffmpeg -i structure.MOV -s 512x512 -vf "rotate=PI" ./frames/%06d.jpg  

for i in `seq 1 2`; do ffmpeg -i $i.webm $i.avi; done  # convert multiple videos
for i in *.avi; do ffmpeg -i "$i" "${i%.*}.mp4"; done  # convert all videos in dir

ffmpeg -i input.mp4 -ss 00:05:20 -t 00:10:00 -c:v copy -c:a copy output1.mp4  # trim a video

```
