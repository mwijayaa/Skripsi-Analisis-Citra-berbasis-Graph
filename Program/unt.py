from skimage import io 
import matplotlib.pyplot as plt
import numpy as np


img = io.imread('img\img001.jpg')
# print(img) # print nilai image original
np.set_printoptions(threshold='nan')
print(img)
print(img.shape)
