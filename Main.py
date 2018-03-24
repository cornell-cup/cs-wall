from GUI import Gui


class Main:
    """Creates GUI and runs it. """

    # initializes the Main object
    def __init__(self):
        print("Main Function Initialized")

    # creates GUI object and runs it infinitely
    def main_function(self):
        print("Start main")

        while True:
            g = Gui()


m = Main()
m.main_function()
