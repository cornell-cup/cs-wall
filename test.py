from GUI import Gui
"""This file tests the GUI by calling methods start_thread/reset_thread to simulate the ECE end of this project. """


class Test:
    g = Gui()

    def __init__(self):
        print "test file"

    def test_start_thread(self):
        # I still think we need a key listener
        self.g.start_thread()
        self.g.make_GUI()


t = Test()
t.test_start_thread()
