# -*- coding: utf-8 -*-
# 显示点云3D图像
from __future__ import print_function
import numpy as np
import pcl
import pcl.pcl_visualization

# load_XYZRGB show pointcloud with color
# load_XYZI show pointcloud without color
cloud = pcl.load_XYZI('unknownCloud.pcd')
visual = pcl.pcl_visualization.CloudViewing()

# ShowColorCloud show pointcloud with color
# ShowGrayCloud show gray pointcloud
visual.ShowGrayCloud(cloud, b'cloud')

flag = True
while flag:
    flag != visual.WasStopped()
end
