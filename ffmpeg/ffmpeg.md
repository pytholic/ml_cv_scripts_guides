```
ffmpeg -i abc.mp4 image%06d.jpg  # extract all frames

ffmpeg -i input.avi output.mp4  # convert video

ffmpeg -i filtering.webm -s 1920x1080 -vsync 2 filtering.mp4  # avoid mp4 issues

ffmpeg -i ./gopro/input/videos/GH011818.MP4 ./gopro/input/frames/GH011818/%06d.jpg  # extract frames

for i in *.webm; do ffmpeg -i "$i" "${i%.*}.mp4"; done  # convert all videos

ffmpeg -i MAX_0042.MP4 -s 1920x1080 -frames:v 500 ./images/%06d.jpg  # -frames:v 500 limites ending frames

ffmpeg -i MAX_0042.MP4 -s 1920x1080  -ss 10 ./images/%06d.jpg  # skip first 10 secs

ffmpeg -i out1.mp4 -vf "select=not(mod(n\,10))" -vsync vfr image_%03d.jpg  # extarct every 10th frame

```
