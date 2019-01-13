#使用类似MATLAB的方法绘制点云的散点图，以可视化点云
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from PointCloudClassification import provider
current_data, current_label = provider.loadDataFile('data/modelnet40_ply_hdf5_2048/ply_data_train0.h5')

points = current_data[7]
# skip = 1   # Skip every n points

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# point_range = range(0, points.shape[0], skip) # skip points to prevent crash
point_range = range(0, points.shape[0]) # skip points to prevent crash
ax.scatter(points[point_range, 0],   # x
           points[point_range, 1],   # y
           points[point_range, 2],   # z
           #c=points[point_range, 2], # height data for color
           cmap='spectral',
           marker="x")
ax.axis('scaled')  # {equal, scaled}
plt.show()