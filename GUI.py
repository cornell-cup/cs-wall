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

    SOUTH = 0
    EAST = 1
    NORTH = 2
    WEST = 3

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

        map = MapMaker()
        # map.parseMap("/test.json")
        self.BOUNDARY_X = map.BOUNDARY_X
        self.GOAL_X = map.GOAL_X
        self.GOAL_Y = map.GOAL_Y
        self.START_X = map.START_X
        self.START_Y = map.START_Y
        self.BOUNDARY_X = 5
        self.START_X = 3
        self.START_Y = 1
        self.robot_x = self.START_X
        self.robot_y = self.START_Y
        self.GOAL_X = 3
        self.GOAL_Y = 4

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
        w, h = 600, 600
        data = np.zeros((h, w, 3), dtype=np.uint8)
        temp_im = Image.open('map.png').convert('RGB')
        data[:600, :600, :] = scipy.misc.imresize(temp_im, (600, 600))
        block_length = 600 / self.BOUNDARY_X
        div_length = 2
        for i in range(0, self.BOUNDARY_X - 1):
            anchor = (i + 1) * block_length
            data[anchor - div_length:anchor + div_length, :, :] = [256, 0, 0]
            data[:, anchor - div_length:anchor + div_length, :] = [256, 0, 0]
        # hanging the target
        target = Image.open('target.png').convert('RGB')
        startx = self.GOAL_X * block_length + (block_length / 4)
        finx = self.GOAL_X * block_length + (3 * block_length / 4)
        starty = self.GOAL_Y * block_length + (block_length / 4)
        finy = self.GOAL_Y * block_length + (3 * block_length / 4)
        data[startx:finx, starty:finy, :] = scipy.misc.imresize(target, (block_length / 2, block_length / 2))
        scipy.misc.imsave('outfile.gif', data)

    # def hang_robot(self, array):
    #     global direction
    #     global robot_x
    #     global robot_y
    #     if direction == SOUTH:
    #         x = 75 + 200 * robot_x
    #         y = 82.5 + 200 * robot_y
    #         array[x:(x + 50), y:(y + 35), :] = Image.open('robot0.png').convert('RGB')
    #     elif direction == EAST:
    #         y = 75 + 200 * robot_y
    #         x = 82.5 + 200 * robot_x
    #         array[x:(x + 35), y:(y + 50), :] = Image.open('robot1.png').convert('RGB')
    #     elif direction == NORTH:
    #         x = 75 + 200 * robot_x
    #         y = 82.5 + 200 * robot_y
    #         array[x:(x + 50), y:(y + 35), :] = Image.open('robot2.png').convert('RGB')
    #     elif direction == WEST:
    #         y = 75 + 200 * robot_y
    #         x = 82.5 + 200 * robot_x
    #         array[x:(x + 35), y:(y + 50), :] = Image.open('robot3.png').convert('RGB')
    #     return array

    def move_robot(self, code):
        if code == "Forward":
            if self.direction == SOUTH:
                self.robot_x += 1
            elif self.direction == EAST:
                self.robot_y += 1
            elif self.direction == NORTH:
                self.robot_x -= 1
            elif self.direction == WEST:
                self.robot_y -= 1
        elif code == "Backward":
            if self.direction == SOUTH:
                self.robot_x -= 1
            elif self.direction == EAST:
                self.robot_y -= 1
            elif self.direction == NORTH:
                self.robot_x += 1
            elif self.direction == WEST:
                self.robot_y += 1
        elif code == "TurnLeft":
            self.direction = (self.direction + 1) % 4
        elif code == "TurnRight":
            self.direction = (self.direction + 3) % 4

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
