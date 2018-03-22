import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from Parser import Parser
from mapMaker import MapMaker
from SystemControl import SystemControl
from Tkinter import Tk, Label, Frame, PhotoImage, Button, Spinbox, Listbox
import tkMessageBox
import scipy.misc
import threading
from moveRobot import moveRobot


# direction 0 is facing south, direction 1 is facing east,
# direction 2 is facing north, and direction 3 is facing west.
class Gui:
    global direction, robot_y, robot_x, index, BOUNDARY_X, GOAL_X, GOAL_Y, START_X, START_Y, WALL_X, WALL_Y
    direction = 1
    robot_x = 0
    robot_y = 0
    index = 0
    BOUNDARY_X = 0
    GOAL_X = 0
    GOAL_Y = 0
    START_X = 0
    START_Y = 0
    WALL_X = 0
    WALL_Y = 0
    level = 1
    version = -1
    TWO_D = 0
    MINIBOT = 1

    def __init__(self):
        global robot_x, robot_y, BOUNDARY_X, GOAL_X, GOAL_Y, START_X, START_Y
        master = Tk()
        master.title("Level Chooser")
        w = Spinbox(master, from_=1, to=10)
        w.pack()
        w.grid(row=0, column=0)

        def store():
            self.level = int(w.get())
            master.destroy()

        level_button = Button(text="ENTER", command=store)
        level_button.pack()
        level_button.grid(row=1, column=0)
        master.mainloop()

        # TODO for MapMaker, we need to add background file name in the json file, and parser, while getting rid of
        # TODO BOUNDARY_Y, WALL_X, WALL_Y.
        map = MapMaker()
        # map.parseMap("/test.json")
        BOUNDARY_X = map.BOUNDARY_X
        GOAL_X = map.GOAL_X
        GOAL_Y = map.GOAL_Y
        START_X = map.START_X
        START_Y = map.START_Y
        BOUNDARY_X = 5
        START_X = 3
        START_Y = 1
        robot_x = START_X
        robot_y = START_Y
        GOAL_X = 3
        GOAL_Y = 4

        p = Parser()
        # a choice box here to choose system (2D or minibot)
        choice = Tk()
        listbox = Listbox(choice)
        listbox.pack()
        listbox.insert(0, "2D System")
        listbox.insert(1, "Minibot")
        listbox.grid(row=0, column=0)

        def store2():
            self.version = listbox.curselection()[0]
            choice.destroy()

        level_button2 = Button(text="ENTER", command=store2)
        level_button2.pack()
        level_button2.grid(row=1, column=0)
        choice.mainloop()
        sc = None
        if self.version == self.TWO_D:
            sc = SystemControl()
        elif self.version == self.MINIBOT:
            sc = moveRobot()
        else:
            temp = Tk()
            temp.withdraw()
            tkMessageBox.showerror("Error", "Please choose a version.")
        self.make_grid()
        root = Tk()
        root.title("WALL")
        Label(root, text="Level " + str(self.level)).grid(row=0, column=1)
        frame = Frame(root)
        im = PhotoImage(file="outfile.gif")
        button = Button(frame, image=im)
        button.pack()

        def start():
            codeblock = p.runCode(p.translateRFID("rfidFOR.txt"))
            if self.version == self.TWO_D:
                if sc.run(codeblock):
                    tkMessageBox.showinfo("Notification", "Congrats! Goal reached!")
                elif not sc.reset_flag:
                    tkMessageBox.showinfo("Notification", "Sorry, incorrect code. Please try again.")
            else:
                sc.run(codeblock)
                if sc.check_goal():
                    tkMessageBox.showinfo("Notification", "Congrats! Goal reached!")
                else:
                    tkMessageBox.showinfo("Notification", "Sorry, incorrect code. Please try again.")

        t = threading.Thread(target=start)

        def start_thread():
            t.start()

        def reset_thread():
            sc.reset_flag = True
            tkMessageBox.showinfo("Notification", "Resetting, please confirm.")
            sc.reset()

        start_button = Button(text="START", command=start_thread)
        start_button.pack()
        reset_button = Button(text="RESET", command=reset_thread)
        reset_button.pack()
        start_button.grid(row=1, column=0)
        reset_button.grid(row=1, column=2)
        frame.pack()
        frame.grid(row=2, columnspan=3)
        root.mainloop()

    # def gallery(self, array, ncols=BOUNDARY_X):
    #     ncols = BOUNDARY_X
    #     nindex, height, width, intensity = array.shape
    #     nrows = nindex//ncols
    #     assert nindex == nrows*ncols
    #     # want result.shape = (height*nrows, width*ncols, intensity)
    #     result = (array.reshape(nrows, ncols, height, width, intensity)
    #               .swapaxes(1,2)
    #               .reshape(height*nrows, width*ncols, intensity))
    #     return result
    #
    # def make_array(self):
    #     return np.array([np.asarray(Image.open('square.gif').convert('RGB'))]*BOUNDARY_X*BOUNDARY_Y)

    def make_grid(self):
        # assuming this is a square grid, which is what we will set it as
        global BOUNDARY_X, GOAL_X, GOAL_Y
        w, h = 600, 600
        data = np.zeros((h, w, 3), dtype=np.uint8)
        temp_im = Image.open('map.png').convert('RGB')
        data[:600, :600, :] = scipy.misc.imresize(temp_im, (600, 600))
        block_length = 600 / BOUNDARY_X
        div_length = 2
        for i in range(0, BOUNDARY_X - 1):
            anchor = (i + 1) * block_length
            data[anchor - div_length:anchor + div_length, :, :] = [256, 0, 0]
            data[:, anchor - div_length:anchor + div_length, :] = [256, 0, 0]
        # hanging the target
        target = Image.open('target.png').convert('RGB')
        startx = GOAL_X * block_length + (block_length / 4)
        finx = GOAL_X * block_length + (3 * block_length / 4)
        starty = GOAL_Y * block_length + (block_length / 4)
        finy = GOAL_Y * block_length + (3 * block_length / 4)
        data[startx:finx, starty:finy, :] = scipy.misc.imresize(target, (block_length / 2, block_length / 2))
        scipy.misc.imsave('outfile.gif', data)

    # def hang_robot(self, array):
    #     global direction
    #     global robot_x
    #     global robot_y
    #     if direction == 0:
    #         x = 75 + 200 * robot_x
    #         y = 82.5 + 200 * robot_y
    #         array[x:(x + 50), y:(y + 35), :] = Image.open('robot0.png').convert('RGB')
    #     elif direction == 1:
    #         y = 75 + 200 * robot_y
    #         x = 82.5 + 200 * robot_x
    #         array[x:(x + 35), y:(y + 50), :] = Image.open('robot1.png').convert('RGB')
    #     elif direction == 2:
    #         x = 75 + 200 * robot_x
    #         y = 82.5 + 200 * robot_y
    #         array[x:(x + 50), y:(y + 35), :] = Image.open('robot2.png').convert('RGB')
    #     elif direction == 3:
    #         y = 75 + 200 * robot_y
    #         x = 82.5 + 200 * robot_x
    #         array[x:(x + 35), y:(y + 50), :] = Image.open('robot3.png').convert('RGB')
    #     return array

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

    # # assuming code is a one-line command
    # def update_once(self, code):
    #     array = self.make_array()
    #     result = self.gallery(array)
    #     self.move_robot(code)
    #     # hanging the target
    #     result[680:720, 880:920, :] = Image.open('target.png').convert('RGB')
    #     self.hang_robot(result)
    #     return result
    #
    # def hang(self, array):
    #     plt.ion()
    #     plt.imshow(array)
    #     plt.pause(0.1)
    #     plt.show()
    #
    # def update(self, code):
    #     global robot_x
    #     global robot_y
    #     list = code.split("\n")
    #     length = len(list)
    #     # self.update_once(code[1])
    #     for i in range(0, length):
    #         code = list[i]
    #         self.hang(self.update_once(code))
    #     if robot_x == GOAL_X:
    #         if robot_y == GOAL_Y:
    #             print "Goal is reached"


g = Gui()
