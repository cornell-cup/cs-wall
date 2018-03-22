from Parser import Parser
import time
# this function is designed to receive movement blocks of Forward, Backward
# TurnLeft, TurnRight and prints corresponding Minibot API
# returns: <<<<SCRIPT,(code)>>>>, a String
# Also note, I don't think that there are parentheses around the code according to their parser


class moveRobot:

    # global reset_flag
    reset_flag = False

    SOUTH = 0
    EAST = 1
    NORTH = 2
    WEST = 3
    robotX = 0
    robotY = 0

    def __init__(self):
        global direction, GoalX, GoalY, dimX, dimY, startX, startY
        direction = 1
        startX = 3
        startY = 1
        self.robotX = startX
        self.robotY = startY
        GoalX = 3
        GoalY = 4
        dimX = 5
        dimY = 5

    # returns one line of the SCRIPT string and a boolean representing whether the target goal is reached
    # TODO to pop off 5 commands at a time, we don't need the "<<<<SCRIPT,>>>>" packaging in this method
    def moveRobot(self, code):
        goal_reached = False
        s = ""
        global direction, GoalX, GoalY
        # TODO change "dummy" to actual power level
        # TODO "dummy" refers to the power needed for minibot to move 1 grid length OR turn
        MOVE_POWER = 50
        TURN_POWER = 50
        # TODO Figure out how long it takes to turn 90 degrees
        TURN_TIME = 3
        if code == "Forward":
            if direction == self.SOUTH:
                self.robotX += 1
            elif direction == self.EAST:
                self.robotY += 1;
            elif direction == self.NORTH:
                self.robotX -= 1;
            elif direction == self.WEST:
                self.robotY -= 1
            s += "<<<<SCRIPT," + "bot.move_forward({})\n".format(MOVE_POWER) + ">>>>\n"
            time = self.calcTravelTime(1, MOVE_POWER)
            s += "<<<<SCRIPT," + "bot.wait({})\n".format(time) + ">>>>\n"
        if code == "Backward":
            if direction == self.SOUTH:
                self.robotX -= 1
            elif direction == self.EAST:
                self.robotY -= 1;
            elif direction == self.NORTH:
                self.robotX += 1;
            elif direction == self.WEST:
                self.robotY += 1
            s += "<<<<SCRIPT," + "bot.move_backward({})\n".format(MOVE_POWER) + ">>>>\n"
            time = self.calcTravelTime(1, MOVE_POWER)
            s += "<<<<SCRIPT," + "bot.wait({})\n".format(time) + ">>>>\n"
        if code == "TurnLeft":
            direction = (direction + 1) % 4
            s += "<<<<SCRIPT," + "bot.move_counter_clockwise({})\n".format(TURN_POWER) + ">>>>\n"
            s += "<<<<SCRIPT," + "bot.wait({})\n".format(TURN_TIME) + ">>>>\n"
        if code == "TurnRight":
            direction = (direction + 3) % 4
            s += "<<<<SCRIPT," + "bot.move_clockwise({})\n".format(TURN_POWER) + ">>>>\n"
            s += "<<<<SCRIPT," + "bot.wait({})\n".format(TURN_TIME) + ">>>>\n"
        if self.robotX == GoalX and self.robotY == GoalY:
            goal_reached = True
        return s, goal_reached

    # checks whether the current position of the robot is out of bounds in the map/maze
    # if the robot is out of bounds, then it resets the position of the robot at its last position in bound
    # returns True if the robot is out of bounds, and False if it is not.
    def checkBounds(self):
        out_of_bounds = False
        global dimX, dimY, direction
        if self.robotX >= dimX:
            out_of_bounds = True
            self.robotX = dimX-1
        elif self.robotX < 0:
            out_of_bounds = True
            self.robotX = 0
        if self.robotY >= dimY:
            out_of_bounds = True
            self.robotY = dimY-1
        elif self.robotY < 0:
            out_of_bounds = True
            self.robotY = 0
        return out_of_bounds

    # returns the finalized SCRIPT string to send to minibot
    def run(self, code):
        s = ""
        # s = "<<<<SCRIPT,"
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
        # s += ">>>>"
        return s

    # sets the direction to NORTH
    def check_dir(self):
        global direction
        if direction == self.NORTH:
            return ""
        elif direction == self.SOUTH:
            return "TurnRight\nTurnRight\n"
        elif direction == self.EAST:
            return "TurnLeft\n"
        elif direction == self.WEST:
            return "TurnRight\n"

    # executing specifically reset()
    def rerun(self, code):
        s = ""
        # s = "<<<<SCRIPT,"
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
        # s += ">>>>"
        return s

    # returns the string to send to minibot for it to revert to its starting point
    def reset(self):
        global startX, startY
        distX = self.robotX - startX
        distY = self.robotY - startY
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
        global GoalX, GoalY
        if self.robotX == GoalX and self.robotY == GoalY:
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
