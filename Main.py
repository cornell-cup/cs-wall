from GUI import Gui


class Main:
    """Creates GUI and runs it. """

    # initializes the Main object
    def __init__(self):
        print("Link Start! XD")

    # creates GUI object and runs it infinitely
    def main_function(self):
        print("Start main")

        while True:
            g = Gui()
            g.make_GUI()

            # while a level is chosen and not passed, the player will remain on that level forever
            while not g.goal_status:
                g.make_game()

            # Once the player finishes that level, he can choose another one!


m = Main()
m.main_function()
