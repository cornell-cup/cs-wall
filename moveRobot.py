# this function is designed to receive movement blocks of Forward, Backward
# TurnLeft, TurnRight and prints corresponding Minibot API
# returns: <<<<SCRIPT,(code)>>>>, a String
# Also note, I don't think that there are parentheses around the code according to their parser
# TODO change "dummy" to actual power level
# TODO "dummy" refers to the power needed for minibot to move 1 grid length OR turn
# TODO figure out minibot's power level and whether we need to use the wait(time) function, also think about connecting
# TODO robotX robotY to an imaginary gui


class moveRobot:

    global direction
    direction = 1
    global robotX
    robotX = 1
    global robotY
    robotY = 3
    global index
    index = 0

    global GoalX
    GoalX = 5
    global GoalY
    GoalY = 5

    SOUTH = 0
    EAST = 1
    NORTH = 2
    WEST = 3

    def __init__(self):
        print "hi"

    def moveRobot(self, code):
        s = "<<<<SCRIPT,"
        global direction
        global robotX
        global robotY
        MOVE_POWER = 50
        TURN_POWER = 50
        TURN_TIME = 3 # TODO Figure out how long it takes to turn 90 degrees
        if code == "Forward":
            if direction == SOUTH:
               robotY += 1
            elif direction == EAST:
                robotX += 1;
            elif direction == NORTH:
              robotY -= 1;
            elif direction == WEST:
                robotX -= 1
            s += "move_forward({})\n".format(MOVE_POWER)
            time = calcTravelTime(1)
            s += "wait({})\n".format(time)
        if code == "Backward":
            if direction == SOUTH:
               robotY -= 1
            elif direction == EAST:
                robotX -= 1;
            elif direction == NORTH:
              robotY += 1;
            elif direction == WEST:
                robotX += 1
            s += "move_backward({})\n".format(MOVE_POWER)
            time = calcTravelTime(1)
            s += "wait({})\n".format(time)
        if code == "TurnLeft":
            direction = (direction + 1) % 4
            s += "move_counter_clockwise({})\n".format(TURN_POWER)
            s += "wait({})\n".format(TURN_TIME)
        if code == "TurnRight":
            direction = (direction + 3) % 4
            s += "move_clockwise({})\n".format(TURN_POWER)
            s += "wait({})\n".format(TURN_TIME)

        s += ">>>>"
        return s

    def calcTravelTime(distance):
        """Returns the amount of [time] Minibot needs to move to go one unit of [distance]"""
        time = 2

        #TODO Calculate travel time based off wheels of Minibot

        return time
