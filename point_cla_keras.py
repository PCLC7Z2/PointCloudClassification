# -*- coding:utf-8 -*-
# author:XueWang
# 读取训练集数据，定义训练集的generator函数，构建神经网络，使用优化函数，tenorboard可视化训练过程，评估训练效果并保存模型到Model文件夹下
import tensorflow as tf
import numpy as np
import sys
import os
import math
import provider
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
from keras.utils import plot_model
from keras.callbacks import TensorBoard
from keras.models import load_model
import time

# \：转译或地址 /：地址
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAIN_DIR = os.path.join(BASE_DIR, r'data/modelnet40_ply_hdf5_2048/train_files.txt')
TRAIN_FILES = provider.getDataFiles(TRAIN_DIR)
TEST_DIR = os.path.join(BASE_DIR, r'data/modelnet40_ply_hdf5_2048/test_files.txt')
TEST_FILES = provider.getDataFiles(TEST_DIR)

NUM_POINT = 2048
BATCH_SIZE = 32
BASE_LEARNING_RATE = 0.001
DirectoryNo = 'K17'

# 1、import data
train_file_idxs = np.arange(0, len(TRAIN_FILES))  #0~len-1
np.random.shuffle(train_file_idxs)  # shuffle the file order
def trainDataPreHandle(train_file_idxs):
	current_data, current_label = provider.loadDataFile(TRAIN_FILES[train_file_idxs])
	# print("load data",current_data.shape,current_label.shape)
	current_data = current_data[:, 0:NUM_POINT, :]  #choose data
	current_data, current_label, _ = provider.shuffle_data(current_data, np.squeeze(current_label))
	current_data = provider.rotate_point_cloud(current_data)
	current_data = provider.jitter_point_cloud(current_data)
	current_data = current_data[:, :, :, np.newaxis]
	current_label = np.squeeze(current_label)	#label
	current_label = keras.utils.to_categorical(current_label, num_classes=40) #40 classes
	return current_data,current_label

def generate_arrays(train_file_idxs):
	while 1:
		for fn in range(len(TRAIN_FILES)-1):
			current_data0,current_label0 = trainDataPreHandle(train_file_idxs[fn]) #get from h5 file and handle it
			batches = current_data0.shape[0]//BATCH_SIZE
			for batch_idx in range(batches):
				start = batch_idx * BATCH_SIZE
				end = (batch_idx+1) * BATCH_SIZE
				current_data = current_data0[start:end,:, :, :]
				current_label = current_label0[start:end,:]
				# print(current_data.shape,current_label.shape,fn,batch_idx)
				yield (current_data,current_label)

#validation data
def generate_validation(train_file_idxs):
	while 1:
		vali_data0,vali_label0 = trainDataPreHandle(train_file_idxs[len(TRAIN_FILES)-1])
		batches = vali_data0.shape[0]//BATCH_SIZE
		for batch_idx in range(batches):
			start = batch_idx * BATCH_SIZE
			end = (batch_idx + 1) * BATCH_SIZE
			vali_data = vali_data0[start:end,:, :, :]
			vali_label = vali_label0[start:end,:]
			yield (vali_data,vali_label)

def getTestData(test_file_idxs):
	test_data, test_label = provider.loadDataFile(TEST_FILES[test_file_idxs[0]])
	test_data = test_data[:, 0:NUM_POINT, :]
	test_data, test_label, _ = provider.shuffle_data(test_data, np.squeeze(test_label))
	test_data = test_data[:, :, :, np.newaxis]
	test_label = np.squeeze(test_label)
	test_label = keras.utils.to_categorical(test_label, num_classes=40)
	return test_data,test_label
test_file_idxs = np.arange(0, len(TEST_FILES))
# np.random.shuffle(test_file_idxs)
test_data,test_label = getTestData(test_file_idxs)


# 2、construct model
model = Sequential()
model.add(Conv2D(64,kernel_size=[1,3],strides=[1,1],padding='valid',activation='relu',input_shape=(NUM_POINT,3,1)))
model.add(Conv2D(64,kernel_size=[1,1],strides=[1,1],padding='valid',activation='relu'))
model.add(Conv2D(128,kernel_size=[1,1],strides=[1,1],padding='valid',activation='relu'))
model.add(Conv2D(512,kernel_size=[1,1],strides=[1,1],padding='valid',activation='relu'))
model.add(Conv2D(1024,kernel_size=[1,1],strides=[1,1],padding='valid',activation='relu'))
model.add(MaxPooling2D(pool_size=(NUM_POINT,1),strides=[2,2],padding='valid'))
model.add(Flatten())
model.add(Dense(512,use_bias=True,activation='relu'))
model.add(Dense(256,use_bias=True))
model.add(Dropout(0.7))
model.add(Dense(40,use_bias=True,activation='softmax'))

# model.add(Conv2D(64, (1, 1), activation='relu', input_shape=(NUM_POINT, 3, 1)))
# model.add(Conv2D(64, (1, 1), activation='relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))
#
# model.add(Conv2D(128, (3, 3), activation='relu'))
# model.add(Conv2D(1024, (3, 3), activation='relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))
#
# model.add(Flatten())
# model.add(Dense(256, activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(10, activation='softmax'))


# 3、active model(optimiser adam)
Adam = keras.optimizers.adam(lr=BASE_LEARNING_RATE, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
model.compile(loss='categorical_crossentropy', optimizer=Adam, metrics=['accuracy'])
#save the log about acc & loss, show in tensorboard
s_time = time.strftime("%Y%m%d%H%M%S", time.localtime())  #timestamp - file time name
logs_path = 'logs/log_%s'%(s_time) + DirectoryNo
try:
	os.makedirs(logs_path)
except:
	pass
tensorboard = TensorBoard(log_dir=logs_path, histogram_freq=0,write_graph=True) #draw line pic


def lrScheduler(epoch):
	if epoch > 120:
		return 0.000001
	if epoch > 80:
		return 0.00001
	if epoch > 60:
		return 0.0001
	else:
		return 0.001
change_lr = keras.callbacks.LearningRateScheduler(lrScheduler) #epoch at 30,lrate decline
lrate = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=10, verbose=0,
								  mode='auto', epsilon=0.0001, cooldown=10, min_lr=0.0000001) #not use
# 4、train model
model.fit_generator(generate_arrays(train_file_idxs),steps_per_epoch=256,epochs=150,verbose=2,callbacks=[tensorboard,change_lr,lrate],
					validation_data=generate_validation(train_file_idxs), validation_steps=64)

# 5、test model
score = model.evaluate(test_data, test_label, BATCH_SIZE)
print(score)
model.save(os.path.join('model/model' + DirectoryNo + '.h5'))
