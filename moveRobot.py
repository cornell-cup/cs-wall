from Parser import Parser
# this function is designed to receive movement blocks of Forward, Backward
# TurnLeft, TurnRight and prints corresponding Minibot API
# returns: <<<<SCRIPT,(code)>>>>, a String
# Also note, I don't think that there are parentheses around the code according to their parser


class moveRobot:

    global direction, robotX, robotY, GoalX, GoalY, dimX, dimY
    direction = 1
    robotX = 1
    robotY = 3
    GoalX = 3
    GoalY = 3
    dimX = 5
    dimY = 5

    SOUTH = 0
    EAST = 1
    NORTH = 2
    WEST = 3

    def __init__(self):
        print "TODO: initialization of dimensions of the map\n"

    # returns one line of the SCRIPT string and a boolean representing whether the target goal is reached
    def moveRobot(self, code):
        goal_reached = False
        s = ""
        global direction, robotX, robotY, GoalX, GoalY
        # TODO change "dummy" to actual power level
        # TODO "dummy" refers to the power needed for minibot to move 1 grid length OR turn
        MOVE_POWER = 50
        TURN_POWER = 50
        # TODO Figure out how long it takes to turn 90 degrees
        TURN_TIME = 3
        if code == "Forward":
            if direction == self.SOUTH:
                robotY += 1
            elif direction == self.EAST:
                robotX += 1;
            elif direction == self.NORTH:
                robotY -= 1;
            elif direction == self.WEST:
                robotX -= 1
            s += "bot.move_forward({})\n".format(MOVE_POWER)
            time = self.calcTravelTime(1, MOVE_POWER)
            s += "bot.wait({})\n".format(time)
        if code == "Backward":
            if direction == self.SOUTH:
                robotY -= 1
            elif direction == self.EAST:
                robotX -= 1;
            elif direction == self.NORTH:
                robotY += 1;
            elif direction == self.WEST:
                robotX += 1
            s += "bot.move_backward({})\n".format(MOVE_POWER)
            time = self.calcTravelTime(1, MOVE_POWER)
            s += "bot.wait({})\n".format(time)
        if code == "TurnLeft":
            direction = (direction + 1) % 4
            s += "bot.move_counter_clockwise({})\n".format(TURN_POWER)
            s += "bot.wait({})\n".format(TURN_TIME)
        if code == "TurnRight":
            direction = (direction + 3) % 4
            s += "bot.move_clockwise({})\n".format(TURN_POWER)
            s += "bot.wait({})\n".format(TURN_TIME)
        if robotX == GoalX and robotY == GoalY:
            goal_reached = True
        return s, goal_reached

    # checks whether the current position of the robot is out of bounds in the map/maze
    # if the robot is out of bounds, then it resets the position of the robot at its last position in bound
    # returns True if the robot is out of bounds, and False if it is not.
    def checkBounds(self):
        out_of_bounds = False
        global robotX, robotY, dimX, dimY, direction
        if robotX >= dimX:
            out_of_bounds = True
            robotX = dimX-1
        elif robotX < 0:
            out_of_bounds = True
            robotX = 0
        if robotY >= dimY:
            out_of_bounds = True
            robotY = dimY-1
        elif robotY < 0:
            out_of_bounds = True
            robotY = 0
        return out_of_bounds

    # returns the finalized SCRIPT string to send to minibot
    def send(self, code):
        global robotX, robotY
        s = "<<<<SCRIPT,"
        list = code.split("\n")
        length = len(list)
        for i in range(0, length):
            code = list[i]
            temp, goal = self.moveRobot(code)
            if self.checkBounds():
                break
            s += temp
        s += ">>>>"
        return s

    # calculates the time needed for the robot to travel a certain distance at a certain power
    def calcTravelTime(self, distance, power):
        """Returns the amount of [time] Minibot needs to move to go one unit of [distance]"""
        time = 2

        # TODO Calculate travel time based off wheels of Minibot
        return time


p = Parser()
codeblock = p.runCode(p.translateRFID("rfidFOR.txt"))
mr = moveRobot()
print mr.send(codeblock)
