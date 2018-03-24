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


class Gui:
    """Creates the WALL GUI according to chosen level. Communicates with the wall and the object (2D system/minibot)
    Throws notifications when designated goal is reached, goal is not reached, and when user fails to provide
    the information needed (i.e. the system the GUI is running on)"""

    direction = 1
    robot_x = 0
    robot_y = 0
    BACKGROUND = ""
    BOUNDARY_X = 0
    GOAL_X = 0
    GOAL_Y = 0
    START_X = 0
    START_Y = 0
    OBS_X = []
    OBS_Y = []
    level = 1
    version = -1
    TWO_D = 0
    MINIBOT = 1

    SOUTH = 0
    EAST = 1
    NORTH = 2
    WEST = 3

    target_file = "image/target.png"
    outfile = "output/outfile.gif"
    obstacle_file = "image/Pirate_Hat.png"

    def __init__(self):
        level_disp = Tk()
        level_disp.title("Level Chooser")
        w = Spinbox(level_disp, from_=1, to=10)
        w.pack()
        w.grid(row=0, column=0)

        # storing the chosen level to local variable
        def store():
            self.level = int(w.get())
            level_disp.destroy()

        level_button = Button(text="ENTER", command=store)
        level_button.pack()
        level_button.grid(row=1, column=0)
        level_disp.mainloop()

        # after level is chosen, variables related to the game level are stored below
        map_data = MapMaker()
        game_data = map_data.parseMap("input/sample_map")
        self.BOUNDARY_X = len(game_data.get("GAME_MAP"))
        self.GOAL_X = game_data.get("GAME_GOAL")[0]
        self.GOAL_Y = game_data.get("GAME_GOAL")[1]
        self.START_X = game_data.get("GAME_START")[0]
        self.START_Y = game_data.get("GAME_START")[1]
        self.robot_x = self.START_X
        self.robot_y = self.START_Y
        self.direction = game_data.get("GAME_START_DIRECTION")
        self.BACKGROUND = game_data.get("GAME_BACKGROUND")

        # getting the coordinates of the map that contains an obstacle (not used or tested yet)
        for row in range(len(game_data.get("GAME_MAP"))):
            for col in range(len(game_data.get("GAME_MAP")[0])):
                if game_data.get("GAME_MAP")[row][col] == 1:
                    self.OBS_X.append(row)
                    self.OBS_Y.append(col)

        p = Parser()
        # making a choice box here to choose system (2D or minibot)
        version_disp = Tk()
        listbox = Listbox(version_disp)
        listbox.pack()
        listbox.insert(0, "2D System")
        listbox.insert(1, "Minibot")
        listbox.grid(row=0, column=0)

        # storing the user's choice of system to local variable
        def store2():
            self.version = listbox.curselection()[0]
            version_disp.destroy()

        version_button = Button(text="ENTER", command=store2)
        version_button.pack()
        version_button.grid(row=1, column=0)
        version_disp.mainloop()
        control = None
        if self.version == self.TWO_D:
            control = SystemControl()
        elif self.version == self.MINIBOT:
            control = moveRobot()
        else:
            temp = Tk()
            temp.withdraw()
            tkMessageBox.showerror("Error", "Please choose a version.")

        control.startX = self.START_X
        control.startY = self.START_Y
        control.GoalX = self.GOAL_X
        control.GoalY = self.GOAL_Y
        control.dimX = self.BOUNDARY_X
        control.dimY = self.BOUNDARY_X
        control.direction = self.direction

        # Constructs the grid according to defined dimensions and displays it on the GUI
        self.make_grid()
        root = Tk()
        root.title("WALL")
        Label(root, text="Level " + str(self.level)).grid(row=0, column=1)
        frame = Frame(root)
        im = PhotoImage(file="image/outfile.gif")
        button = Button(frame, image=im)
        button.pack()

        # runs the given file of rfid's
        def start():
            codeblock = p.runCode(p.translateRFID("input/rfidFOR.txt"))
            if self.version == self.TWO_D:
                if control.run(codeblock):
                    tkMessageBox.showinfo("Notification", "Congrats! Goal reached!")
                elif not control.reset_flag:
                    tkMessageBox.showinfo("Notification", "Sorry, incorrect code. Please try again.")
            else:
                control.run(codeblock)
                if control.check_goal():
                    tkMessageBox.showinfo("Notification", "Congrats! Goal reached!")
                elif not control.reset_flag:
                    tkMessageBox.showinfo("Notification", "Sorry, incorrect code. Please try again.")

        t = threading.Thread(target=start)

        # runs the method start()
        def start_thread():
            t.start()

        # stops the processing of the rfid's and returns the robot to the starting point
        def reset_thread():
            control.reset_flag = True
            tkMessageBox.showinfo("Notification", "Resetting, please confirm.")
            control.reset()

        # making the buttons (start/reset) on the GUI
        start_button = Button(text="START", command=start_thread)
        start_button.pack()
        reset_button = Button(text="RESET", command=reset_thread)
        reset_button.pack()
        start_button.grid(row=1, column=0)
        reset_button.grid(row=1, column=2)
        frame.pack()
        frame.grid(row=2, columnspan=3)
        root.mainloop()

    # divides the given background image into given number of blocks, saves the image to outfile.gif in the directory
    def make_grid(self):
        w, h = 600, 600
        data = np.zeros((h, w, 3), dtype=np.uint8)
        temp_im = Image.open(self.BACKGROUND).convert('RGB')
        data[:600, :600, :] = scipy.misc.imresize(temp_im, (600, 600))
        block_length = 600 / self.BOUNDARY_X
        div_length = 2
        for i in range(0, self.BOUNDARY_X - 1):
            anchor = (i + 1) * block_length
            data[anchor - div_length:anchor + div_length, :, :] = [256, 0, 0]
            data[:, anchor - div_length:anchor + div_length, :] = [256, 0, 0]
        # hanging the target
        target = Image.open(self.target_file).convert('RGB')
        startx = self.GOAL_X * block_length + (block_length / 4)
        finx = self.GOAL_X * block_length + (3 * block_length / 4)
        starty = self.GOAL_Y * block_length + (block_length / 4)
        finy = self.GOAL_Y * block_length + (3 * block_length / 4)
        data[startx:finx, starty:finy, :] = scipy.misc.imresize(target, (block_length / 2, block_length / 2))
        scipy.misc.imsave(self.outfile, data)

        # TODO hang obstacles
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

    # def move_robot(self, code):
    #     if code == "Forward":
    #         if self.direction == 0:
    #             self.robot_x += 1
    #         elif self.direction == 1:
    #             self.robot_y += 1
    #         elif self.direction == 2:
    #             self.robot_x -= 1
    #         elif self.direction == 3:
    #             self.robot_y -= 1
    #     elif code == "Backward":
    #         if self.direction == 0:
    #             self.robot_x -= 1
    #         elif self.direction == 1:
    #             self.robot_y -= 1
    #         elif self.direction == 2:
    #             self.robot_x += 1
    #         elif self.direction == 3:
    #             self.robot_y += 1
    #     elif code == "TurnLeft":
    #         self.direction = (self.direction + 1) % 4
    #     elif code == "TurnRight":
    #         self.direction = (self.direction + 3) % 4

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
