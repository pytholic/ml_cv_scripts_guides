# Notes
## Problem statement
Used to estimate 3D location of points in the environment. We have a bunch of points in 3D that we don't know the position of. We project them onto 2D plane of the `camera` and we took several photos and we are interested to find the position of the `points` in 3D.
In addition to the `location` of the points, we also want to estimate where the camera was or `camera poses` while taking those images. 

## How does BA work?
**Assumption** - We can estimate features from our image data (SIFT features, corners etc.). We assume that we are able to extarct distinct points in our images, and then we are only using these points in order to perform our 3D reconstruction task.



# Links
https://www.youtube.com/watch?v=lmj2Jk5tl60
