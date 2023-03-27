"""
Script to visualize the results. It requires "points.ply" and "camera.ply" files.
If you applied outlier removal, then use "output.ply" instead of "points.ply".
You will require 'Open3D' for this.
"""

import os
import time

import open3d as o3d


PATH = "./results"  # path to input folder


# Create visualizer
vis = o3d.visualization.VisualizerWithKeyCallback()
vis.create_window()


ZOOM = 1  # default zoom value


#pcd = o3d.io.read_point_cloud(os.path.join(PATH, "points.ply"))  # without outlier removal
pcd = o3d.io.read_point_cloud(os.path.join(PATH, 'output.ply'))  # with outlier removal
poses = o3d.io.read_line_set(os.path.join(PATH, "camera.ply"))


# Add to the visualizer
vis.add_geometry(pcd)
vis.add_geometry(poses)
vis.poll_events()
vis.update_renderer()


# Utility functions
def zoom_in(vis):
    global ZOOM
    # print('zoom in')
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


# Initial setup
view_ctl = vis.get_view_control()
view_ctl.set_up((0, -1, 0))
view_ctl.set_zoom(0.5)


# Define callback functions
vis.register_key_callback(ord("W"), zoom_in)
vis.register_key_callback(ord("S"), zoom_out)

vis.register_key_callback(ord("A"), rotate_view_left)
vis.register_key_callback(ord("D"), rotate_view_right)

vis.register_key_callback(ord("Q"), rotate_view_up)
vis.register_key_callback(ord("E"), rotate_view_down)


# Ru nthe visualizer
vis.run()
vis.destroy_window()
