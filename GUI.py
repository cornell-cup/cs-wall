import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


class Gui:
    direction = 1
    robot_x = 3
    robot_y = 1

    def __init__(self):
        print("hi")

    def gallery(self, array, ncols=5):
        nindex, height, width, intensity = array.shape
        nrows = nindex//ncols
        assert nindex == nrows*ncols
        # want result.shape = (height*nrows, width*ncols, intensity)
        result = (array.reshape(nrows, ncols, height, width, intensity)
                  .swapaxes(1,2)
                  .reshape(height*nrows, width*ncols, intensity))
        return result

    def make_array(self):
        return np.array([np.asarray(Image.open('square.gif').convert('RGB'))]*25)

    def hang_robot(self, array):
        if self.direction == 0:
            x = 75 + 200 * self.robot_x
            y = 82.5 + 200 * self.robot_y
            array[x:(x + 50), y:(y + 35), :] = Image.open('robot0.png').convert('RGB')
        elif self.direction == 1:
            y = 75 + 200 * self.robot_y
            x = 82.5 + 200 * self.robot_x
            array[x:(x + 35), y:(y + 50), :] = Image.open('robot1.png').convert('RGB')
        elif self.direction == 2:
            x = 75 + 200 * self.robot_x
            y = 82.5 + 200 * self.robot_y
            array[x:(x + 50), y:(y + 35), :] = Image.open('robot2.png').convert('RGB')
        elif self.direction == 3:
            y = 75 + 200 * self.robot_y
            x = 82.5 + 200 * self.robot_x
            array[x:(x + 35), y:(y + 50), :] = Image.open('robot3.png').convert('RGB')
        return array

    def move_robot(self, code):
        if code == "Forward":
            if self.direction == 0:
                self.robot_x += 1
            elif self.direction == 1:
                self.robot_x += 1
            elif self.direction == 2:
                self.robot_y -= 1
            elif self.direction == 3:
                self.robot_y -= 1
        elif code == "Backward":
            if self.direction == 0:
                self.robot_x -= 1
            elif self.direction == 1:
                self.robot_x -= 1
            elif self.direction == 2:
                self.robot_y += 1
            elif self.direction == 3:
                self.robot_y += 1
        elif code == "TurnLeft":
            self.direction = (self.direction + 1) % 4
        elif code == "TurnRight":
            self.direction = (self.direction + 3) % 4


g = Gui()
array = g.make_array()
result = g.gallery(array)
# hanging the target
result[680:720, 880:920, :] = Image.open('target.png').convert('RGB')
result = g.hang_robot(result)
plt.imshow(result)
plt.show()
