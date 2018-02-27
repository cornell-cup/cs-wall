import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from Parser import Parser


# direction 0 is facing south, direction 1 is facing east,
# direction 2 is facing north, and direction 3 is facing west.
class Gui:
    global direction
    direction = 1
    global robot_x
    robot_x = 3
    global robot_y
    robot_y = 1
    global index
    index = 0

    def __init__(self):
        array = self.make_array()
        result = self.gallery(array)
        # hanging the target
        result[680:720, 880:920, :] = Image.open('target.png').convert('RGB')
        result = self.hang_robot(result)
        plt.imshow(result)
        plt.show()

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
        global direction
        global robot_x
        global robot_y
        if direction == 0:
            x = 75 + 200 * robot_x
            y = 82.5 + 200 * robot_y
            array[x:(x + 50), y:(y + 35), :] = Image.open('robot0.png').convert('RGB')
        elif direction == 1:
            y = 75 + 200 * robot_y
            x = 82.5 + 200 * robot_x
            array[x:(x + 35), y:(y + 50), :] = Image.open('robot1.png').convert('RGB')
        elif direction == 2:
            x = 75 + 200 * robot_x
            y = 82.5 + 200 * robot_y
            array[x:(x + 50), y:(y + 35), :] = Image.open('robot2.png').convert('RGB')
        elif direction == 3:
            y = 75 + 200 * robot_y
            x = 82.5 + 200 * robot_x
            array[x:(x + 35), y:(y + 50), :] = Image.open('robot3.png').convert('RGB')
        return array

    def move_robot(self, code):
        global direction
        global robot_x
        global robot_y

        if code == "Forward":
            if direction == 0:
                robot_x += 1
            elif direction == 1:
                robot_y += 1
            elif direction == 2:
                robot_x -= 1
            elif direction == 3:
                robot_y -= 1
        elif code == "Backward":
            if direction == 0:
                robot_x -= 1
            elif direction == 1:
                robot_y -= 1
            elif direction == 2:
                robot_x += 1
            elif direction == 3:
                robot_y += 1
        elif code == "TurnLeft":
            direction = (direction + 1) % 4
        elif code == "TurnRight":
            direction = (direction + 3) % 4

    # assuming code is a one-line command
    def update_once(self, code):
        array = self.make_array()
        result = self.gallery(array)
        self.move_robot(code)
        # hanging the target
        result[680:720, 880:920, :] = Image.open('target.png').convert('RGB')
        self.hang_robot(result)
        return result

    def hang(self, array):
        plt.ion()
        plt.imshow(array)
        plt.pause(0.1)
        plt.show()

    def update(self, code):
        list = code.split("\n")
        length = len(list)
        # self.update_once(code[1])
        for i in range(0, length):
            code = list[i]
            self.hang(self.update_once(code))


g = Gui()
p = Parser()
codeblock = p.runCode(p.translateRFID("rfidFOR.txt"))
g.update(codeblock)
