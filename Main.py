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
        # Collect events until released
        with keyboard.Listener(on_press=self.on_press(),
                               on_release=self.on_release()) as listener:
            listener.join()

        print("Listener made")

        while True:
            print("anything")
            g = Gui()
            p = Parser()
            codeblock = p.runCode(p.translateRFID("rfidFOR.txt"))
            sc = SystemControl()
            # print sc.run(codeblock)


    def on_press(key):
        try:
            print('alphanumeric key {0} pressed'.format(key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def on_release(key):
        print('{0} released'.format(key))

        if key == keyboard.Key.esc:
            # Stop listener
            return False

m = Main()
m.main_function()

