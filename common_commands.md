```sh
# Extract frames with size and rotation
# rotation = PI, PI/2 etc.
ffmpeg -i structure.MOV -s 512x512 -vf "rotate=PI" ./frames/%06d.jpg  

for i in `seq 1 2`; do ffmpeg -i $i.webm $i.avi; done  # convert multiple videos
```
