import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def gallery(array, ncols=5):
    nindex, height, width, intensity = array.shape
    nrows = nindex//ncols
    assert nindex == nrows*ncols
    # want result.shape = (height*nrows, width*ncols, intensity)
    result = (array.reshape(nrows, ncols, height, width, intensity)
              .swapaxes(1,2)
              .reshape(height*nrows, width*ncols, intensity))
    return result


def make_array():
    return np.array([np.asarray(Image.open('square.gif').convert('RGB'))]*25)


array = make_array()
result = gallery(array)
result[:50, :35, :] = Image.open('robot0.png').convert('RGB')
plt.imshow(result)
plt.show()
