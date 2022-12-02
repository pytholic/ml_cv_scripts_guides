```
ffmpeg -i abc.mp4 image%06d.jpg  # extract all frames

ffmpeg -i input.avi output.mp4  # convert video

ffmpeg -i filtering.webm -s 1920x1080 -vsync 2 filtering.mp4  # avoid mp4 issues

ffmpeg -i ./gopro/input/videos/GH011818.MP4 ./gopro/input/frames/GH011818/%06d.jpg  # extract frames

for i in *.webm; do ffmpeg -i "$i" "${i%.*}.mp4"; done  # convert all videos


```
