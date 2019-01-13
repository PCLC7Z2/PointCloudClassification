import numpy as np
arr = np.array([[1,2,3],[3,4,5],[4,5,6]])
# arr = np.array([1,2,3])
col = arr[0].size
i = 1
for x in np.nditer(arr):
    i = i%col
    print(x, end=" ")
    if i==0: print("\n",end="") #print默认换行
    i = i+1
