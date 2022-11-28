# NeRF Steps

**Preprocess**

Put video in folder and run.

```
python3 /home/pytholic/Desktop/Projects/uav_mapping/instant-ngp/scripts/colmap2nerf.py --video_in elevator.MOV --video_fps 10 --run_colmap --aabb_scale 16
```
or use images

```
python3 /home/pytholic/Desktop/Projects/uav_mapping/instant-ngp/scripts/colmap2nerf.py --images /home/pytholic/Desktop/Projects/uav_mapping/data/iphone/tmp/tmp --run_colmap --aabb_scale 16
```

**Run nerf**

Give path to folder.

```
./build/testbed --scene data/custom_data/ios/elevator
```

**Loading snapshot**

```
./build/testbed --scene data/custom_data/ios/office --snapshot data/custom_data/ios/office/base.msgpack
```

**Generate video**

[https://www.youtube.com/watch?v=8GbENSmdVeE](https://www.youtube.com/watch?v=8GbENSmdVeE)

```
python scripts/run.py --mode nerf --scene data/nerf/fox --load_snapshot data/custom_data/ios/office/base.msgpack --video_camera_path data/custom_data/ios/office/base_cam.json --video_n_seconds 5 --video_fps 10 --width 1920 --height 1080
```

---

# Droid SLAM

```
conda activate drodienv
python demo.py --imagedir=<>path --calib=<path>
python demo.py --imagedir=data/abandonedfactory --calib=calib/tartan.txt --reconstruction_path <>
python demo.py --imagedir=/hdd/pytholic/droid_slam/data/evo/input/frames/MAX_0040 --calib=calib/evo.txt --reconstruction_path /hdd/pytholic/droid_slam/data/evo/result/reconstructions/MAX_0040 --disable_vis
```
