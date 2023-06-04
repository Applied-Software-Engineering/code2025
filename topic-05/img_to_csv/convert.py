import numpy as np
from PIL import Image

# read image
im = Image.open("test.png")

# convert to numpy array
arr = np.array(im)
# output shape via print
print(arr.shape)

# convert 3d array to 2d list of lists
arr = arr.reshape(arr.shape[0], -1).tolist()
# output shape via print
print(len(arr), len(arr[0]))

# save list of lists to csv
np.savetxt("test.csv", arr, delimiter=",")
