from Parser import Parser
from SystemControl import SystemControl
from GUI import Gui

class Main():

    def __init__(self):
        print "Main Function Initialized"

    def main_function(self):
        while True:
            print "anything"
            g = Gui()
            p = Parser()
            codeblock = p.runCode(p.translateRFID("rfidFOR.txt"))
            sc = SystemControl()
            # print sc.run(codeblock)

m = Main()
m.main_function()

