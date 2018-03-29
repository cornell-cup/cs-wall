from random import *
import numpy as np
from PIL import Image
from Parser import Parser
from mapMaker import MapMaker
from SystemControl import SystemControl
from Tkinter import Tk, Label, Frame, PhotoImage, Button, Spinbox, Listbox
import tkMessageBox
import scipy.misc
import threading
from moveRobot import moveRobot
import Globals as G


class Gui:
    """Creates the WALL GUI according to chosen level. Communicates with the wall and the object (2D system/minibot)
    Throws notifications when designated goal is reached, goal is not reached, and when user fails to provide
    the information needed (i.e. the system the GUI is running on)"""

    direction = 1
    BACKGROUND = ""
    BOUNDARY = 0
    GOAL_X = 0
    GOAL_Y = 0
    START_X = 0
    START_Y = 0
    init_OBS = []
    OBS = []
    level = 1
    version = -1
    TWO_D = 0
    MINIBOT = 1

    control = None

    rfid_file = "input/rfidFOR.txt"
    target_file = "image/target.png"
    outfile = "image/outfile.gif"
    obstacle_file = "image/Pirate_Hat.png"
    bot0_file = "image/robot0.png"
    bot1_file = "image/robot1.png"
    bot2_file = "image/robot2.png"
    bot3_file = "image/robot3.png"

    temp_image = ""

    def __init__(self):
        level_disp = Tk()
        level_disp.title("Level Chooser")
        w = Spinbox(level_disp, from_=1, to=10)
        w.grid(row=0, column=0)

        # storing the chosen level to local variable
        def store():
            self.level = int(w.get())
            level_disp.destroy()

        level_button = Button(text="ENTER", command=store)
        level_button.grid(row=1, column=0)
        level_disp.mainloop()

        # after level is chosen, variables related to the game level are stored below
        map_data = MapMaker()
        game_data = map_data.parseMap("input/sample_map")
        self.BOUNDARY = len(game_data.get("GAME_MAP"))
        self.GOAL_X = game_data.get("GAME_GOAL")[0]
        self.GOAL_Y = game_data.get("GAME_GOAL")[1]
        self.START_X = game_data.get("GAME_START")[0]
        self.START_Y = game_data.get("GAME_START")[1]
        self.robot_x = self.START_X
        self.robot_y = self.START_Y
        self.direction = game_data.get("GAME_START_DIRECTION")
        self.BACKGROUND = game_data.get("GAME_BACKGROUND")

        # getting the coordinates of the map that contains an obstacle
        for row in range(len(game_data.get("GAME_MAP"))):
            for col in range(len(game_data.get("GAME_MAP")[0])):
                # 1 represents obstacle, 0 represents free space.
                if game_data.get("GAME_MAP")[row][col] == 1:
                    self.init_OBS.append([row, col])
                    self.OBS.append([row, col])

        p = Parser()
        # making a choice box here to choose system (2D or minibot)
        version_disp = Tk()
        listbox = Listbox(version_disp)
        listbox.insert(0, "2D System")
        listbox.insert(1, "Minibot")
        listbox.grid(row=0, column=0)

        # storing the user's choice of system to local variable
        def store2():
            self.version = listbox.curselection()[0]
            version_disp.destroy()

        version_button = Button(text="ENTER", command=store2)
        version_button.grid(row=1, column=0)
        version_disp.mainloop()

        if self.version == self.TWO_D:
            self.control = SystemControl()
        elif self.version == self.MINIBOT:
            self.control = moveRobot()
        else:
            temp = Tk()
            temp.withdraw()
            tkMessageBox.showerror("Error", "Please choose a version.")

        # storing the map data from mapMaker to the class variables of control
        self.control.startX = self.START_X
        self.control.startY = self.START_Y
        self.control.GoalX = self.GOAL_X
        self.control.GoalY = self.GOAL_Y
        self.control.dimX = self.BOUNDARY
        self.control.dimY = self.BOUNDARY
        self.control.start_dir = self.direction
        self.control.direction = self.control.start_dir
        self.control.OBS = self.OBS

        # Constructs the grid according to defined dimensions and displays it on the GUI
        self.make_grid()
        root = Tk()
        root.title("WALL")
        label = Label(root, text="Level " + str(self.level))
        label.grid(row=0, column=1)
        frame = Frame(root)
        self.temp_image = self.outfile
        im = PhotoImage(file=self.temp_image)
        im_label = Label(frame, image=im)
        im_label.pack()

        # updates the grid according to the robot's current location/direction
        def update():
            if t.is_alive():
                self.make_grid()
                # updates locations of the obstacles for next second
                self.move_obs_random()
                self.control.OBS = self.OBS

                self.temp_image = self.outfile
                tempim = PhotoImage(file=self.temp_image)
                # changes image here
                im_label.config(image=tempim)
                im_label.image = tempim
                im_label.pack()
                # updates display every 2 seconds
            root.after(2000, update)

        # runs the given file of rfid's
        def start():
            codeblock = p.runCode(p.translateRFID(self.rfid_file))
            if self.version == self.TWO_D:
                if self.control.run(codeblock, self.OBS):
                    tkMessageBox.showinfo("Notification", "Congrats! Goal reached!")
                elif not self.control.reset_flag:
                    tkMessageBox.showinfo("Notification", "Sorry, incorrect code. Please try again.")
            else:
                self.control.run(codeblock)
                if self.control.check_goal():
                    tkMessageBox.showinfo("Notification", "Congrats! Goal reached!")
                elif not self.control.reset_flag:
                    tkMessageBox.showinfo("Notification", "Sorry, incorrect code. Please try again.")

        t = threading.Thread(target=start)

        # runs the method start()
        def start_thread():
            t.start()

        # stops the processing of the rfid's and returns the robot to the starting point
        def reset_thread():
            self.control.reset_flag = True
            tkMessageBox.showinfo("Notification", "Resetting, please confirm.")
            self.control.reset()
            self.OBS = self.init_OBS
            self.make_grid()
            self.temp_image = self.outfile
            tempim = PhotoImage(file=self.temp_image)
            # changes image here
            im_label.config(image=tempim)
            im_label.image = tempim
            im_label.pack()

        # making the buttons (start/reset) on the GUI
        start_button = Button(text="START", command=start_thread)
        reset_button = Button(text="RESET", command=reset_thread)
        start_button.grid(row=1, column=0)
        reset_button.grid(row=1, column=2)
        frame.grid(row=2, columnspan=3)
        update()
        root.mainloop()

    # divides the given background image into given number of blocks, saves the image to outfile.gif in the directory
    def make_grid(self):
        w, h = 600, 600
        data = np.zeros((h, w, 3), dtype=np.uint8)
        temp_im = Image.open(self.BACKGROUND).convert('RGB')
        data[:600, :600, :] = scipy.misc.imresize(temp_im, (600, 600))
        block_length = 600 / self.BOUNDARY
        div_length = 2
        for i in range(0, self.BOUNDARY - 1):
            anchor = (i + 1) * block_length
            data[anchor - div_length:anchor + div_length, :, :] = [256, 0, 0]
            data[:, anchor - div_length:anchor + div_length, :] = [256, 0, 0]

        # hanging the target
        self.hang_square_object(data, block_length, self.target_file, self.GOAL_X, self.GOAL_Y)
        # hanging the obstacles
        for i in range(len(self.OBS)):
            self.hang_square_object(data, block_length, self.obstacle_file, self.OBS[i][0], self.OBS[i][1])
        # hanging robot
        self.hang_robot(block_length, data)
        scipy.misc.imsave(self.outfile, data)

    # hangs the designated object on the GUI (either the target or the obstacle(s))
    def hang_square_object(self, array, block_length, filename, x, y):
        target = Image.open(filename).convert('RGB')
        startx = x * block_length + (block_length / 4)
        finx = x * block_length + (3 * block_length / 4)
        starty = y * block_length + (block_length / 4)
        finy = y * block_length + (3 * block_length / 4)
        array[startx:finx, starty:finy, :] = scipy.misc.imresize(target, (block_length / 2, block_length / 2))

    # hangs the robot according to its current position
    def hang_robot(self, block_length, array):
        if self.control.direction == G.SOUTH:
            self.hang_square_object(array, block_length, self.bot0_file, self.control.robotX, self.control.robotY)
        elif self.control.direction == G.EAST:
            self.hang_square_object(array, block_length, self.bot1_file, self.control.robotX, self.control.robotY)
        elif self.control.direction == G.NORTH:
            self.hang_square_object(array, block_length, self.bot2_file, self.control.robotX, self.control.robotY)
        elif self.control.direction == G.WEST:
            self.hang_square_object(array, block_length, self.bot3_file, self.control.robotX, self.control.robotY)

    # checks whether a single random move of the robot is feasible, ie not out of bounds and not overlapping
    def check_random(self, pseudo_x, pseudo_y):
        # check whether it is out of bounds or overlapping with another obstacle, which are not allowed
        allowed = False
        if pseudo_x < 0 or pseudo_y < 0 or pseudo_x >= self.BOUNDARY or pseudo_y >= self.BOUNDARY:
            # check if it is out of bounds
            return allowed
        else:
            # check if it is overlapping with the obstacles
            if [pseudo_x, pseudo_y] in self.OBS:
                return allowed
            allowed = True
        return allowed

    # moves the obstacle randomly
    def move_obs_random(self):
        # possible movements: north, south, east, west, attack
        for i in range(len(self.OBS)):
            allowed = False
            while not allowed:
                index = randint(1, 5)
                if index == 1:
                    # move north
                    temp_x = self.OBS[i][0] - 1
                    temp_y = self.OBS[i][1]
                    if self.check_random(temp_x, temp_y):
                        self.OBS[i][0] = temp_x
                        allowed = True
                elif index == 2:
                    # move south
                    temp_x = self.OBS[i][0] + 1
                    temp_y = self.OBS[i][1]
                    if self.check_random(temp_x, temp_y):
                        self.OBS[i][0] = temp_x
                        allowed = True
                elif index == 3:
                    # move east
                    temp_x = self.OBS[i][0]
                    temp_y = self.OBS[i][1] + 1
                    if self.check_random(temp_x, temp_y):
                        self.OBS[i][1] = temp_y
                        allowed = True
                elif index == 4:
                    # move west
                    temp_x = self.OBS[i][0]
                    temp_y = self.OBS[i][1] - 1
                    if self.check_random(temp_x, temp_y):
                        self.OBS[i][1] = temp_y
                        allowed = True
                elif index == 5:
                    # TODO
                    # attack
                    print "attack"


g = Gui()
