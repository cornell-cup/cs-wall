import numpy as np
import matplotlib.pyplot as plt

def gallery(array, ncols=3):
    nindex, height, width, intensity = array.shape
    nrows = nindex//ncols
    assert nindex == nrows*ncols
    # want result.shape = (height*nrows, width*ncols, intensity)
    result = (array.reshape(nrows, ncols, height, width, intensity)
              .swapaxes(1,2)
              .reshape(height*nrows, width*ncols, intensity))
    return result

def make_array():
    import Image
    return np.array([np.asarray(Image.open('face.png').convert('RGB'))]*12)

array = make_array()
result = gallery(array)
plt.imshow(result)
plt.show()