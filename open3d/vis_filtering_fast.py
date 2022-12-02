import os
import time
import numpy as np

import open3d as o3d

from functools import partial
from collections import defaultdict


# Define paths and variables

PATH = "./results"
ZOOM = 1

# Colors rgb
# COLORS = {
#         "person": [117,255,126],  # green
#         "toy_car": [255,54,41],  # red
#         "toy_plane": [185,119,14],  # brown
#         "toy_tank": [255,0,255],  # pink
#         "toy_truck": [117,177,255]  # blue
# }

# Colors hex
COLORS = {
    "person": "#75ff7e",  # green
    "toy_car": "#ff3629",  # red
    "toy_plane": "#B9770E",  # brown
    "toy_tank": "#FF00FF",  # pink
    "toy_truck": "#75b1ff",  # blue
}

# Utility functions


def hex2rgb(h):
    """
    Function to convert hex into rgb
    """
    return tuple(int(h[1 + i : 1 + i + 2], 16) for i in (0, 2, 4))


def denormalize(x: int):
    """
    Function to denormalize the pixel values.
    """
    return x * 255


def normalize(x: tuple):
    """
    Function to normalize pixel values.
    """
    x = list(map(lambda n: n / 255, x))
    return x


def is_close(a, b):
    """
    Function to check if pixel values are approximately same.
    """
    tmp = np.isclose(a, b, atol=5)  # 1
    if False not in tmp:
        return True
    else:
        return False


def get_indices(pcd, category):
    """
    Function to collect indices of a category from point cloud for filtering.
    """
    indices = []
    for i, color in enumerate(pcd.colors):
        color = denormalize(color)  # denormalize
        color2 = hex2rgb(COLORS[category])
        res = is_close(list(color), color2)
        if res == True:
            indices.append(i)

    return indices


def filter(vis, cls):
    """
    Function to filter the desired objects.
    """

    global cnt_dict
    cnt_dict[cls] += 1

    # Set mask color if count is odd
    if cnt_dict[cls] % 2 != 0:
        for k, v in idx_dict.items():
            if k != cls:
                for idx in v:
                    pcd.colors[idx] = [0.9, 0.9, 0.9]  # light gray color
        print(f"{cls} filtering done...")

    # Set default color if count is even
    else:
        for k, v in idx_dict.items():
            for idx in v:
                pcd.colors[idx] = normalize(hex2rgb(COLORS[k]))

        print(f"{cls} filtering removed...")

    vis.update_geometry(pcd)
    print(cnt_dict[cls])


def show_original(vis):
    """
    Function to reset and show original point cloud.
    """

    global cnt_dict

    for k, v in idx_dict.items():
        for i in v:
            pcd.colors[i] = normalize(hex2rgb(COLORS[k]))

    cnt_dict = {key: 0 for key in cnt_dict}  # set counts to 0

    print("Showing original...")
    vis.update_geometry(pcd)


def zoom_in(vis):
    global ZOOM
    view_ctl = vis.get_view_control()
    ZOOM -= 0.03
    view_ctl.set_zoom(ZOOM)
    return False


def zoom_out(vis):
    global ZOOM
    view_ctl = vis.get_view_control()
    ZOOM += 0.03
    view_ctl.set_zoom(ZOOM)
    return False


def rotate_view_left(vis):
    ctr = vis.get_view_control()
    ctr.rotate(5.0, 0.0)
    return False


def rotate_view_right(vis):
    ctr = vis.get_view_control()
    ctr.rotate(-5.0, 0.0)
    return False


def rotate_view_up(vis):
    ctr = vis.get_view_control()
    ctr.rotate(0.0, -5.0)
    return False


def rotate_view_down(vis):
    ctr = vis.get_view_control()
    ctr.rotate(0.0, 5.0)
    return False


# Read point clouds
pcd = o3d.io.read_point_cloud(os.path.join(PATH, "output.ply"))
poses = o3d.io.read_line_set(os.path.join(PATH, "camera.ply"))

print("Starting points collection...")

# Create counter and indices dict
cnt_dict = defaultdict()  # defaultdict for easy increment
idx_dict = dict()  # save background indices for each class
for k, v in COLORS.items():
    cnt_dict[k] = 0
    idx_dict[k] = get_indices(pcd, k)
    print(f"{k} points collection done!")

print("Collection finished!")


# Visualization
vis = o3d.visualization.VisualizerWithKeyCallback()
vis.create_window()


view_ctl = vis.get_view_control()
view_ctl.set_up((0, -1, 0))
view_ctl.set_zoom(0.5)

vis.register_key_callback(ord("W"), zoom_in)
vis.register_key_callback(ord("S"), zoom_out)

vis.register_key_callback(ord("A"), rotate_view_left)
vis.register_key_callback(ord("D"), rotate_view_right)

vis.register_key_callback(ord("Q"), rotate_view_up)
vis.register_key_callback(ord("E"), rotate_view_down)

for i, (k, v) in enumerate(COLORS.items()):
    vis.register_key_callback(ord(str(i)), partial(filter, cls=k))

vis.register_key_callback(ord("`"), show_original)

vis.add_geometry(pcd)
vis.add_geometry(poses)
vis.poll_events()
vis.update_renderer()

vis.run()
vis.destroy_window()
