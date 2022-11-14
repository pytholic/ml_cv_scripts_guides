"""
Script to apply outlier removal algorithm.
You can chose between Statistical or Radial outlier removal.
You might have to tune the parameters to get good results.
"""

import os

import open3d as o3d

PATH = "./results"

pcd = o3d.io.read_point_cloud(os.path.join(PATH, "points.ply"))
o3d.visualization.draw_geometries([pcd])
print("Oulier removal...")

# Apply statuscal outlie removal
# cl, ind = pcd.remove_statistical_outlier(nb_neighbors=100, std_ratio=1)

# Apply radial outler removal
cl, ind = pcd.remove_radius_outlier(nb_points=20, radius=0.03)  # 0.07

# Display results
o3d.visualization.draw_geometries([cl])
o3d.io.write_point_cloud(os.path.join(PATH, "output.ply"), cl)
