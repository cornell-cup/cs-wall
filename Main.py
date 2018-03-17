from Parser import Parser
from SystemControl import SystemControl
from GUI import Gui
from pynput.keyboard import Key, Listener
from pynput import keyboard
class Main():

    def __init__(self):
        print "Main Function Initialized"
        global reset_flag
        reset_flag = False

    def main_function(self):
        print("Start main")

        while True:
            print("anything")
            g = Gui()
            p = Parser()
            codeblock = p.runCode(p.translateRFID("rfidFOR.txt"))
            sc = SystemControl()
            print sc.run(codeblock)


m = Main()
print("Listener made")
#
# def on_press(key):
#     print("pressed!!")
#
# def on_release(key):
#     print("released!!")
#
# with keyboard.Listener(on_press=on_press,
#                        on_release=on_release) as listener:
#     listener.join()
m.main_function()

