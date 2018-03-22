from Parser import Parser
import time
# this function is designed to receive movement blocks of Forward, Backward
# TurnLeft, TurnRight and prints corresponding Minibot API
# returns: <<<<SCRIPT,(code)>>>>, a String
# Also note, I don't think that there are parentheses around the code according to their parser


class moveRobot:

    reset_flag = False
    SOUTH = 0
    EAST = 1
    NORTH = 2
    WEST = 3
    robotX = 0
    robotY = 0
    direction = 1
    GoalX = 0
    GoalY = 0
    dimX = 0
    dimY = 0
    startX = 0
    startY = 0

    def __init__(self):
        self.startX = 3
        self.startY = 1
        self.robotX = self.startX
        self.robotY = self.startY
        self.GoalX = 3
        self.GoalY = 4
        self.dimX = 5
        self.dimY = 5

    # returns one line of the SCRIPT string and a boolean representing whether the target goal is reached
    # TODO to pop off 5 commands at a time, we don't need the "<<<<SCRIPT,>>>>" packaging in this method
    def moveRobot(self, code):
        goal_reached = False
        s = ""
        # TODO change "dummy" to actual power level
        # TODO "dummy" refers to the power needed for minibot to move 1 grid length OR turn
        MOVE_POWER = 50
        TURN_POWER = 50
        # TODO Figure out how long it takes to turn 90 degrees
        TURN_TIME = 3
        if code == "Forward":
            if self.direction == self.SOUTH:
                self.robotX += 1
            elif self.direction == self.EAST:
                self.robotY += 1;
            elif self.direction == self.NORTH:
                self.robotX -= 1;
            elif self.direction == self.WEST:
                self.robotY -= 1
            s += "<<<<SCRIPT," + "bot.move_forward({})\n".format(MOVE_POWER) + ">>>>\n"
            time = self.calcTravelTime(1, MOVE_POWER)
            s += "<<<<SCRIPT," + "bot.wait({})\n".format(time) + ">>>>\n"
        if code == "Backward":
            if self.direction == self.SOUTH:
                self.robotX -= 1
            elif self.direction == self.EAST:
                self.robotY -= 1;
            elif self.direction == self.NORTH:
                self.robotX += 1;
            elif self.direction == self.WEST:
                self.robotY += 1
            s += "<<<<SCRIPT," + "bot.move_backward({})\n".format(MOVE_POWER) + ">>>>\n"
            time = self.calcTravelTime(1, MOVE_POWER)
            s += "<<<<SCRIPT," + "bot.wait({})\n".format(time) + ">>>>\n"
        if code == "TurnLeft":
            self.direction = (self.direction + 1) % 4
            s += "<<<<SCRIPT," + "bot.move_counter_clockwise({})\n".format(TURN_POWER) + ">>>>\n"
            s += "<<<<SCRIPT," + "bot.wait({})\n".format(TURN_TIME) + ">>>>\n"
        if code == "TurnRight":
            self.direction = (self.direction + 3) % 4
            s += "<<<<SCRIPT," + "bot.move_clockwise({})\n".format(TURN_POWER) + ">>>>\n"
            s += "<<<<SCRIPT," + "bot.wait({})\n".format(TURN_TIME) + ">>>>\n"
        if self.robotX == self.GoalX and self.robotY == self.GoalY:
            goal_reached = True
        return s, goal_reached

    # checks whether the current position of the robot is out of bounds in the map/maze
    # if the robot is out of bounds, then it resets the position of the robot at its last position in bound
    # returns True if the robot is out of bounds, and False if it is not.
    def checkBounds(self):
        out_of_bounds = False
        if self.robotX >= self.dimX:
            out_of_bounds = True
            self.robotX = self.dimX-1
        elif self.robotX < 0:
            out_of_bounds = True
            self.robotX = 0
        if self.robotY >= self.dimY:
            out_of_bounds = True
            self.robotY = self.dimY-1
        elif self.robotY < 0:
            out_of_bounds = True
            self.robotY = 0
        return out_of_bounds

    # returns the finalized SCRIPT string to send to minibot
    def run(self, code):
        s = ""
        list = code.split("\n")
        length = len(list)
        for i in range(0, length):
            if not self.reset_flag:
                code = list[i]
                temp, goal = self.moveRobot(code)
                if self.checkBounds():
                    break
                if temp != "":
                    s += temp
                print temp
                time.sleep(1)
            else:
                s += self.reset()
                break
        return s

    # sets the direction to NORTH
    def check_dir(self):
        if self.direction == self.NORTH:
            return ""
        elif self.direction == self.SOUTH:
            return "TurnRight\nTurnRight\n"
        elif self.direction == self.EAST:
            return "TurnLeft\n"
        elif self.direction == self.WEST:
            return "TurnRight\n"

    # executing specifically reset()
    def rerun(self, code):
        s = ""
        list = code.split("\n")
        length = len(list)
        for i in range(0, length):
            code = list[i]
            temp, goal = self.moveRobot(code)
            if self.checkBounds():
                break
            if temp != "":
                s += temp
            print temp
            # time.sleep(1)
        return s

    # returns the string to send to minibot for it to revert to its starting point
    def reset(self):
        distX = self.robotX - self.startX
        distY = self.robotY - self.startY
        s = ""
        if distX == 0 and distY == 0:
            return ""
        if distX > 0:
            # go north
            s += self.check_dir()
            for i in range(0, distX):
                s += "Forward\n"
        elif distX < 0:
            # go south
            s += self.check_dir()
            for i in range(0, distX):
                s += "Backward\n"
        if distY > 0:
            # go west
            s += self.check_dir() + "TurnLeft\n"
            for i in range(0, distY):
                s += "Forward\n"
        elif distY < 0:
            # go east
            s += self.check_dir() + "TurnRight\n"
            for i in range(0, distY):
                s += "Forward\n"
        return self.rerun(s)

    def check_goal(self):
        if self.robotX == self.GoalX and self.robotY == self.GoalY:
            return True
        return False

    # calculates the time needed for the robot to travel a certain distance at a certain power
    def calcTravelTime(self, distance, power):
        """Returns the amount of [time] Minibot needs to move to go one unit of [distance]"""
        time = 2

        # TODO Calculate travel time based off wheels of Minibot
        return time


# p = Parser()
# codeblock = p.runCode(p.translateRFID("rfidFOR.txt"))
# mr = moveRobot()
# print mr.run(codeblock)
