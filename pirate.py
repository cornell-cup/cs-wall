class Pirate:

    # the pirate's location in the grid in the form of [x, y]
    location = []
    # defines if the pirate is movable or not depending on the type of game
    movable = False

    def __init__(self, x, y):
        # initiates the pirate's location as input [x, y]
        self.location = [x, y]
