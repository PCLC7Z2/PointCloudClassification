# -*- coding:utf-8 -*-
# author:ChengZheng

import numpy as np
import pcl
import provider
import random

current_data, current_label = provider.loadDataFile('data/modelnet40_ply_hdf5_2048/ply_data_test1.h5')
# print(current_data[0])  #numpy.ndarray
# print(type(current_data[0][1].tostring())) #class 'bytes'
filename = 'unknownCloud.h5'

pointCloudObject = ['airplane','bathtub','bed','bench','bookshelf','bottle','bowl','car','chair','cone',
      'cup','curtain','desk','door','dresser','flower_pot','glass_box','guitar','keyboard','lamp',
      'laptop','mantel','monitor','night_stand','person','piano','plant','radio','range_hood','sink',
      'sofa','stairs','stool','table','tent','toilet','tv_stand','vase','wardrobe','xbox']

# 通过改变current_data[1]的值读出不一样的点云
no = 4
current_data_one = current_data[no-1]
print(pointCloudObject[current_label[no-1][0]])
f_prefix = filename.split('.')[0]
output_filename = '{prefix}.pcd'.format(prefix=f_prefix)
output = open(output_filename,"w+")

header = '# .PCD v0.7 - Point Cloud Data file format\nVERSION 0.7\nFIELDS x y z\nSIZE 4 4 4\nTYPE F F F' \
             '\nCOUNT 1 1 1\nWIDTH 2048\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0\nPOINTS 2048\nDATA ascii\n'

output.write(header)

col = current_data_one[0].size
i = 1
for x in np.nditer(current_data_one):
    i = i % col
    output.write(str(x)+" ")
    if i==0:
        output.write("\n")
    i = i+1

output.close()

# show PointCloud
import os
os.system("python showCloud.py")
