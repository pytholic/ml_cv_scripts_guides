import os
import time
import open3d as o3d

#root_folder = '/home/pytholic/Desktop/Projects/uav_mapping/droid_slam/results/my_results/evo/reconstructions/tmp'
root_folder = '/home/pytholic/Desktop/Projects/uav_mapping/droid_slam/results/my_results/iphone/reconstructions/tables/office/desk_1'
files_list = sorted(os.listdir(root_folder))
files = [i for i in files_list if i.endswith('.ply')]
# print(files)

vis = o3d.visualization.VisualizerWithKeyCallback()
vis.create_window()

zoom = 1
for file in files:
    if file.split('/')[-1] == "points.ply":
        pcd = o3d.io.read_point_cloud(os.path.join(root_folder, file))
    elif file.split('/')[-1] == "camera.ply":
        pcd = o3d.io.read_line_set(os.path.join(root_folder, file))
    vis.add_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()
    #time.sleep(1)



def zoom_in(vis):
    global zoom
    # print('zoom in')
    view_ctl = vis.get_view_control()
    zoom -= .03
    view_ctl.set_zoom(zoom)
    return False

def zoom_out(vis):
    global zoom
    view_ctl = vis.get_view_control()
    zoom += .03
    view_ctl.set_zoom(zoom)
    return False

def rotate_view_left(vis):
    ctr = vis.get_view_control()
    ctr.rotate(5.0, 0.0)
    return False
def rotate_view_right(vis):
    ctr = vis.get_view_control()
    ctr.rotate(- 5.0, 0.0)
    return False

def rotate_view_up(vis):
    ctr = vis.get_view_control()
    ctr.rotate(0.0, -5.0)
    return False
def rotate_view_down(vis):
    ctr = vis.get_view_control()
    ctr.rotate(0.0, 5.0)
    return False




view_ctl = vis.get_view_control()
view_ctl.set_up((0, -1, 0))
view_ctl.set_zoom(.5)

vis.register_key_callback(ord("W"), zoom_in)
vis.register_key_callback(ord("S"), zoom_out)

vis.register_key_callback(ord("A"), rotate_view_left)
vis.register_key_callback(ord("D"), rotate_view_right)

vis.register_key_callback(ord("Q"), rotate_view_up)
vis.register_key_callback(ord("E"), rotate_view_down)
# vis.register_key_callback(ord("S"), zoom_out)
#vis.get_render_option().load_from_json("./renderoption.json")
vis.run()
vis.destroy_window()