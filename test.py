from GUI import Gui
from pynput.keyboard import Key, Controller
"""This file tests the GUI by calling methods start_thread/reset_thread to simulate the ECE end of this project. """


class Test:
    g = Gui()

    def __init__(self):
        print ("test file")

    def test_GUI(self):
        """Now we have a key listener. What the ECE part needs I guess is just to simulate key presses with
        {k = Controller()
        k.press(Key.cmd)/(Key.shift)}
        where cmd is the key for start and shift is the key for reset. At the head of their class, before
        any button presses, they need to make a GUI object and call make_GUI()"""
        self.g.make_GUI()


t = Test()
t.test_GUI()
