from PIL import Image
import numpy as np
import scipy.misc


w, h = 600, 600
data = np.zeros((h, w, 3), dtype=np.uint8)
temp_im = Image.open('map.png').convert('RGB')
data[:600, :600, :] = scipy.misc.imresize(temp_im, (600, 600))
num_blocks = 5
block_length = 600 / num_blocks
div_length = 2
for i in range(0, num_blocks):
    anchor = (i+1) * block_length
    data[anchor - div_length:anchor + div_length, :, :] = [256, 0, 0]
    data[:, anchor - div_length:anchor + div_length, :] = [256, 0, 0]
img = Image.fromarray(data, 'RGB')
img.show()
