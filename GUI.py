import numpy as np
from PIL import Image
from Parser import Parser
from mazeMaker import MapMaker
from SystemControl import SystemControl
from Tkinter import Tk, Label, Frame, PhotoImage, Button, Spinbox, Listbox
import tkMessageBox
import scipy.misc
import threading
from moveRobot import moveRobot
import Globals as G
from pynput import keyboard
from pirate import Pirate
from pirateMapMaker import PirateMapMaker
# import RPi.GPIO as GPIO
# import a4988


class Gui:
    """Creates the WALL GUI according to chosen level. Communicates with the wall and the object (2D system/minibot)
    Throws notifications when designated goal is reached, goal is not reached, and when user fails to provide
    the information needed (i.e. the system the GUI is running on)"""

    # basic stats
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
    game = -1
    game_name = ""
    version = -1
    TWO_D = 0
    MINIBOT = 1
    MAZE = 0
    PIRATES = 1

    # conditional stats
    dead_pirates = []

    # conditional objects
    control = None
    t = None

    # flags
    start_flag = False
    thread_started = False
    dead_flag = False

    # file paths
    # TODO change to "rfidAttack1.txt" later.
    rfid_file = "input/rfidAttack.txt"
    target_file = "image/target.png"
    outfile = "image/outfile.gif"
    obstacle_file = "image/Pirate_Hat.png"
    dead_pirates_file = "image/dead_pirate.png"
    path1_file = "image/path1.png"
    path2_file = "image/path2.png"
    path3_file = "image/path3.png"
    path4_file = "image/path4.png"
    bot0_file = "image/robot0.png"
    bot1_file = "image/robot1.png"
    bot2_file = "image/robot2.png"
    bot3_file = "image/robot3.png"
    temp_image = ""

    def __init__(self):
        """initializes the GUI status to the following: start status to False, prompts for game version, system
        version, and level. """
        self.start_flag = False
        game_disp = Tk()
        game_disp.title("Game Chooser")
        listbox = Listbox(game_disp)
        listbox.pack()
        listbox.insert(0, "Maze")
        listbox.insert(1, "Pirates")
        listbox.grid(row=0, column=0)

        def store3():
            """storing the user's choice of system to local variable"""
            self.game = listbox.curselection()[0]
            game_disp.destroy()

        # stores the type of game in a string (maze/pirates)
        game_button = Button(text="ENTER", command=store3)
        game_button.grid(row=1, column=0)
        game_disp.mainloop()

        if self.game == self.MAZE:
            self.game_name = "maze"
        elif self.game == self.PIRATES:
            self.game_name = "pirate"
        else:
            temp1 = Tk()
            temp1.withdraw()
            tkMessageBox.showerror("Error", "Please choose a game.")

        # making a choice box here to choose system (2D or minibot)
        version_disp = Tk()
        version_disp.title("Version Chooser")
        listbox = Listbox(version_disp)
        listbox.pack()
        listbox.insert(0, "2D System")
        listbox.insert(1, "Minibot")
        listbox.grid(row=0, column=0)

        def store2():
            """storing the user's choice of system to local variable"""
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

        # allows the player to choose a level from a spinbox (need to change to buttons in the future)
        level_disp = Tk()
        level_disp.title("Level Chooser")
        w = Spinbox(level_disp, from_=1, to=10)
        w.grid(row=0, column=0)

        def store():
            """storing the chosen level to local variable"""
            self.level = int(w.get())
            level_disp.destroy()

        level_button = Button(text="ENTER", command=store)
        level_button.grid(row=1, column=0)
        level_disp.mainloop()

    def store_game_data(self):
        """after level is chosen, variables related to the game level are stored below"""
        game_data = {}

        if self.game == self.MAZE:
            map_data = MapMaker()
            game_data = map_data.parseMap("levels/" + self.game_name + "_levels/" + self.game_name + "_" +
                                          str(self.level))
            # game_data = map_data.parseMap("input/sample_map")
            self.BOUNDARY = len(game_data.get("GAME_MAP"))
            self.init_OBS = []
            self.OBS = []

            # getting the coordinates of the map that contains an obstacle
            for row in range(len(game_data.get("GAME_MAP"))):
                for col in range(len(game_data.get("GAME_MAP")[0])):
                    # 1 represents obstacle, 0 represents free space.
                    if game_data.get("GAME_MAP")[row][col] == 1:
                        pirate = Pirate(row, col)
                        pirate.movable = False
                        self.init_OBS.append(pirate)
                        self.OBS.append(pirate)

        elif self.game == self.PIRATES:
            map_data = PirateMapMaker()
            game_data = map_data.parseMap("levels/" + self.game_name + "_levels/" + self.game_name + "_" +
                                          str(self.level))
            self.BOUNDARY = len(game_data.get("GAME_MAP"))
            self.init_OBS = []
            self.OBS = []

            for index in range(len(game_data.get("GAME_ENEMIES"))):
                temp_data = game_data.get("GAME_ENEMIES")[index]
                temp_path = temp_data.get("ENEMY_PATH")
                pirate = Pirate(temp_path[0][0], temp_path[0][1])
                pirate2 = Pirate(temp_path[0][0], temp_path[0][1])
                pirate.movable = True
                pirate2.movable = True
                pirate.path = temp_path
                pirate2.path = temp_path
                self.init_OBS.append(pirate2)
                self.OBS.append(pirate)

        self.GOAL_X = game_data.get("GAME_GOAL")[0]
        self.GOAL_Y = game_data.get("GAME_GOAL")[1]
        self.START_X = game_data.get("GAME_START")[0]
        self.START_Y = game_data.get("GAME_START")[1]
        self.direction = game_data.get("GAME_START_DIRECTION")
        self.BACKGROUND = game_data.get("GAME_BACKGROUND")

        # storing the map data from mapMaker to the class variables of control
        self.control.startX = self.START_X
        self.control.startY = self.START_Y
        self.control.robotX = self.START_X
        self.control.robotY = self.START_Y
        self.control.GoalX = self.GOAL_X
        self.control.GoalY = self.GOAL_Y
        self.control.dimX = self.BOUNDARY
        self.control.start_dir = self.direction
        self.control.direction = self.control.start_dir
        self.control.OBS = self.OBS

    def make_GUI(self):
        """makes the GUI"""
        self.store_game_data()

        self.make_grid()
        """Constructs the grid according to defined dimensions and displays it on the GUI"""
        root = Tk()
        root.title("WALL")
        label = Label(root, text="Level " + str(self.level))
        label.grid(row=0, column=1)
        frame = Frame(root)
        self.temp_image = self.outfile
        im = PhotoImage(file=self.temp_image)
        im_label = Label(frame, image=im)
        im_label.pack()

        step_label = Label(root, text="Time Step: " + str(self.control.time_step))
        step_label.grid(row=0, column=2)

        def update():
            """updates the grid according to the robot's current location/direction"""
            self.make_grid()
            step_label.config(text="Time Step: " + str(self.control.time_step))
            self.temp_image = self.outfile
            tempim = PhotoImage(file=self.temp_image)
            # changes image here
            im_label.config(image=tempim)
            im_label.image = tempim
            im_label.pack()

            # updates display every 1 second
            root.after(1000, update)

        def on_press(key):
            """defines what the key listener does
            NOTE: Now the ECE end does not have to call a method, they need to simulate key presses."""
            try:
                k = key.char  # single-char keys
            except:
                k = key.name  # other keys
            if key == keyboard.Key.esc:
                return False  # stop listener
            if k in ['ctrl']:  # keys interested
                # self.keys.append(k) # store it in global-like variable
                print('Key pressed: ' + k)
                if not self.thread_started:
                    self.t = threading.Thread(target=start)
                    self.thread_started = True
                    self.start_flag = True
                else:
                    if self.dead_flag:
                        self.t = None
                        self.t = threading.Thread(target=start)
                        self.start_flag = True
                        self.dead_flag = False
            if k in ['shift']:
                print('Key pressed: ' + k)
                if not self.control.reset_flag:
                    self.control.reset_flag = True
                    tkMessageBox.showinfo("Notification", "Resetting, please confirm.")
                    self.control.reset()
                    self.control.time_step = 0
                    self.OBS = self.init_OBS
                    self.control.OBS = self.init_OBS
                    self.dead_pirates = []
                    self.control.dead_pirates = []
                    self.start_flag = False
                    self.dead_flag = True
                    self.control.reset_flag = False
                # return False

        def start():
            """runs the given file of rfid's"""
            # a4988.init()
            p = Parser()
            codeblock = p.runCode(p.translateRFID(self.rfid_file))
            if self.version == self.TWO_D:
                if self.control.run(codeblock, self.OBS, self.dead_pirates):
                    tkMessageBox.showinfo("Notification", "Congrats! Goal reached!")
                    self.level += 1
                    if not self.level > G.MAX_LEVEL:
                        self.store_game_data()
                        self.dead_flag = True
                    else:
                        tkMessageBox.showinfo("Notification", "All levels cleared")
                elif not self.control.reset_flag:
                    tkMessageBox.showinfo("Notification", "Sorry, incorrect code. Please try again.")
                    self.control.reset()
                    self.control.time_step = 0
                    self.OBS = self.init_OBS
                    self.control.OBS = self.init_OBS
                    self.dead_pirates = []
                    self.control.dead_pirates = []
                    self.make_grid()
                    self.temp_image = self.outfile
                    tempim = PhotoImage(file=self.temp_image)
                    # changes image here
                    im_label.config(image=tempim)
                    im_label.image = tempim
                    im_label.pack()
                    self.dead_flag = True
            else:
                self.control.run(codeblock)
                if self.control.check_goal():
                    tkMessageBox.showinfo("Notification", "Congrats! Goal reached!")
                    self.level += 1
                    if not self.level > G.MAX_LEVEL:
                        self.store_game_data()
                        self.dead_flag = True
                    else:
                        tkMessageBox.showinfo("Notification", "All levels cleared")
                elif not self.control.reset_flag:
                    tkMessageBox.showinfo("Notification", "Sorry, incorrect code. Please try again.")
                    self.control.reset()
                    self.control.time_step = 0
                    self.OBS = self.init_OBS
                    self.control.OBS = self.init_OBS
                    self.dead_pirates = []
                    self.control.dead_pirates = []
                    self.make_grid()
                    self.temp_image = self.outfile
                    tempim = PhotoImage(file=self.temp_image)
                    # changes image here
                    im_label.config(image=tempim)
                    im_label.image = tempim
                    im_label.pack()
                    self.dead_flag = True

        lis = keyboard.Listener(on_press=on_press)
        lis.start()
 
        #  # Motor Scanner Setup
        #  stepPin1 = 2
        #  dirPin1 = 3
        #  enablePin1 = 18
        #  sleepPin1 = 4
        #
        #  GPIO.setup(stepPin1, GPIO.OUT)
        #  GPIO.setup(dirPin1, GPIO.OUT)
        #  GPIO.setup(enablePin1, GPIO.OUT)
        #  GPIO.setup(sleepPin1, GPIO.OUT)
        #
        #  GPIO.output(enablePin1, GPIO.LOW)
        #  GPIO.output(sleepPin1, GPIO.LOW)
        #  GPIO.output(dirPin1, GPIO.HIGH)
        #
        #  #Motor Vertical
        #  stepPin2 = 27
        #  dirPin2 = 22
        #  enablePin2 = 23
        #  sleepPin2 = 17
        #
        #  GPIO.setup(stepPin2, GPIO.OUT)
        #  GPIO.setup(dirPin2, GPIO.OUT)
        #  GPIO.setup(enablePin2, GPIO.OUT)
        #  GPIO.setup(sleepPin2, GPIO.OUT)
        #
        #  GPIO.output(enablePin2, GPIO.LOW)
        #  GPIO.output(sleepPin2, GPIO.LOW)
        #  GPIO.output(dirPin2, GPIO.HIGH)
        #
        #  #Motor Horizontal
        #  stepPin3 = 9
        #  dirPin3 = 11
        #  enablePin3 = 24
        #  sleepPin3 = 10
        #
        #  GPIO.setup(stepPin3, GPIO.OUT)
        #  GPIO.setup(dirPin3, GPIO.OUT)
        #  GPIO.setup(enablePin3, GPIO.OUT)
        #  GPIO.setup(sleepPin3, GPIO.OUT)
        #
        #  GPIO.output(enablePin3, GPIO.LOW)
        #  GPIO.output(sleepPin3, GPIO.LOW)
        #  GPIO.output(dirPin3, GPIO.HIGH)
        #
        #  start_button = 6
        #  reset_button = 5
        #  scanner_top_pin = 21
        #  scanner_bottom_pin = 26
        #  horizontal_top_pin = 16
        #  horizontal_bottom_pin = 20
        #  vertical_top_pin = 13
        #  vertical_bottom_pin=19
        #
        #  GPIO.setup(start_button, GPIO.IN)
        #  GPIO.setup(reset_button, GPIO.IN)
        #  GPIO.setup(scanner_top_pin, GPIO.IN)
        #  GPIO.setup(scanner_bottom_pin, GPIO.IN)
        #  GPIO.setup(horizontal_top_pin, GPIO.IN)
        #  GPIO.setup(horizontal_bottom_pin, GPIO.IN)
        #  GPIO.setup(vertical_top_pin, GPIO.IN)
        #  GPIO.setup(vertical_bottom_pin, GPIO.IN)
        #
        # def reset(reset_button):
        #     if not self.control.reset_flag:
        #         print ('reset')
        #         self.control.reset_flag = True
        #         tkMessageBox.showinfo("Notification", "Resetting, please confirm.")
        #         self.control.reset()
        #         self.control.time_step = 0
        #         self.OBS = self.init_OBS
        #         self.control.OBS = self.init_OBS
        #         self.dead_pirates = []
        #         self.control.dead_pirates = []
        #          self.start_flag = False
        #          self.dead_flag = True
        #          self.control.reset_flag = False
        #
        #  def start(start_button):
        #      if not self.thread_started:
        #          self.t = threading.Thread(target=start)
        #          self.thread_started = True
        #          self.start_flag = True
        #      else:
        #          if self.dead_flag:
        #              self.t = None
        #              self.t = threading.Thread(target=start)
        #              self.start_flag = True
        #              self.dead_flag = False
        #
        #  def stop1(scanner_top_pin):
        #      print(' scanner, hit top')
        #      a4988.moveScannerDown(25)
        #      GPIO.output(enablePin1, GPIO.HIGH) #disable driver
        #
        #
        #  def stop2(scanner_bottom_pin):
        #      print('scanner, hit bottom')
        #      a4988.moveScannerUp(25)
        #      GPIO.output(enablePin1, GPIO.HIGH) #disable driver
        #
        #
        #  def stop3(horizontal_top_pin):
        #      print('horizontal , hit top bound')
        #      a4988.moveHorizontalDown(25)
        #      GPIO.output(enablePin1, GPIO.HIGH) #disable driver
        #
        #
        #  def stop4(horizontal_bottom_pin):
        #      print('horizontal , hit bottom bound')
        #      a4988.moveHorizontalUp(25)
        #      GPIO.output(enablePin1, GPIO.HIGH) #disable driver
        #
        #
        #  def stop5(vertical_top_pin):
        #      print('vertical , hit top bound')
        #      a4988.moveVerticalDown(25)
        #      GPIO.output(enablePin1, GPIO.HIGH) #disable driver
        #
        #
        #  def stop6(vertical_bottom_pin):
        #      print('vertical , hit bottom bound')
        #      a4988.moveVerticalUp(25)
        #      GPIO.output(enablePin1, GPIO.HIGH) #disable driver
        #
        #
        #  GPIO.add_event_detect(start_button, GPIO.FALLING, callback=start, bouncetime=2000)
        #  GPIO.add_event_detect(reset_button, GPIO.FALLING, callback=reset, bouncetime=2000)
        # # GPIO.add_event_detect(scanner_bottom_pin, GPIO.FALLING, callback=stop1, bouncetime=2000)
        #  GPIO.add_event_detect(scanner_top_pin, GPIO.FALLING, callback=stop2, bouncetime=2000)
        #  GPIO.add_event_detect(horizontal_top_pin, GPIO.FALLING, callback=stop3, bouncetime=2000)
        #  GPIO.add_event_detect(horizontal_bottom_pin, GPIO.FALLING, callback=stop4, bouncetime=2000)
        #  GPIO.add_event_detect(vertical_top_pin, GPIO.FALLING, callback=stop5, bouncetime=2000)
        #  GPIO.add_event_detect(vertical_bottom_pin, GPIO.FALLING, callback=stop6, bouncetime=2000)

        def check_status():
            """checks every second whether the start button has been pressed"""
            if self.start_flag:
                if not self.control.reset_flag:
                    self.t.start()
                    self.start_flag = False

            root.after(1000, check_status)

        frame.grid(row=2, columnspan=4)
        update()
        check_status()
        root.mainloop()

    def make_grid(self):
        """divides the given background image into given number of blocks, saves the image to outfile.gif
        in the directory"""
        w, h = 600, 600
        data = np.zeros((h, w, 3), dtype=np.uint8)
        temp_im = Image.open(self.BACKGROUND).convert('RGB')
        data[:600, :600, :] = scipy.misc.imresize(temp_im, (600, 600))
        block_length = 600 / self.BOUNDARY
        div_length = 2
        for i in range(0, self.BOUNDARY - 1):
            anchor = (i + 1) * block_length
            data[anchor - div_length:anchor + div_length, :, :] = [192, 192, 192]
            data[:, anchor - div_length:anchor + div_length, :] = [192, 192, 192]

        # hanging the target
        self.hang_square_object(data, block_length, self.target_file, self.GOAL_X, self.GOAL_Y)

        # hanging the obstacles
        for i in range(len(self.OBS)):
            self.hang_square_object(data, block_length, self.obstacle_file, self.OBS[i].location[0],
                                    self.OBS[i].location[1])

        # hanging the killed obstacles
        for i in range(len(self.dead_pirates)):
            self.hang_square_object(data, block_length, self.dead_pirates_file, self.dead_pirates[i][0],
                                    self.dead_pirates[i][1])

        # path added to the graph
        for i in range(len(self.OBS)):
            temp_obs = self.OBS[i]
            for j in range(len(temp_obs.path)-1):
                loc1 = temp_obs.path[j]
                loc2 = temp_obs.path[j+1]
                self.hang_path(data, block_length, loc1[0], loc1[1], loc2[0], loc2[1])
        
        # hanging robot
        self.hang_robot(block_length, data)
        scipy.misc.imsave(self.outfile, data)

    def hang_path(self, array, block_length, x1, y1, x2, y2):
        """hangs the designated object on the GUI (either the target or the obstacle(s))"""
        if x1 == x2:
            # horizontal
            if y1 < y2:
                filename = self.path2_file
            else:
                y1 = y2
                filename = self.path1_file
            target = Image.open(filename).convert('RGB')
            startx = x1 * block_length + (block_length / 4) + (1 * block_length / 4)
            finx = x1 * block_length + (block_length / 4) + (1 * block_length / 4) + (block_length / 2 / 10)
            starty = y1 * block_length + (block_length / 4) + (2 * block_length / 4)
            finy = y1 * block_length + (block_length / 4) + (2 * block_length / 4) + (block_length / 2)
            array[startx:finx, starty:finy, :] = scipy.misc.imresize(target, (block_length / 2 / 10, block_length / 2))
        else:
            # vertical
            if x1 < x2:
                filename = self.path4_file
            else:
                x1 = x2
                filename = self.path3_file
            target = Image.open(filename).convert('RGB')
            startx = x1 * block_length + (3 * block_length / 4)
            finx = x1 * block_length + (3 * block_length / 4) + (block_length / 2)
            starty = y1 * block_length + (2 * block_length / 4)
            finy = y1 * block_length + (2 * block_length / 4) + (block_length / 2 / 10)
            array[startx:finx, starty:finy, :] = scipy.misc.imresize(target, (block_length / 2, block_length / 2 / 10))

    def hang_square_object(self, array, block_length, filename, x, y):
        """hangs the designated object on the GUI (either the target or the obstacle(s))"""
        target = Image.open(filename).convert('RGB')
        startx = x * block_length + (block_length / 4)
        finx = x * block_length + (3 * block_length / 4)
        starty = y * block_length + (block_length / 4)
        finy = y * block_length + (3 * block_length / 4)
        array[startx:finx, starty:finy, :] = scipy.misc.imresize(target, (block_length / 2, block_length / 2))

    def hang_robot(self, block_length, array):
        """hangs the robot according to its current position"""
        if self.control.direction == G.SOUTH:
            self.hang_square_object(array, block_length, self.bot0_file, self.control.robotX, self.control.robotY)
        elif self.control.direction == G.EAST:
            self.hang_square_object(array, block_length, self.bot1_file, self.control.robotX, self.control.robotY)
        elif self.control.direction == G.NORTH:
            self.hang_square_object(array, block_length, self.bot2_file, self.control.robotX, self.control.robotY)
        elif self.control.direction == G.WEST:
            self.hang_square_object(array, block_length, self.bot3_file, self.control.robotX, self.control.robotY)


g = Gui()
g.make_GUI()
