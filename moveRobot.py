import Globals as G
import time


class moveRobot:
    """Packages the translated RFID's received from Wall through Parser as minibot script in the form of
    "<<<<SCRIPT, code>>>>" and sends it to minibot. In addition, records the current position of the bot during
    its movement as class variables. """

    reset_flag = False
    start_dir = 1
    robotX = 0
    robotY = 0
    direction = start_dir
    GoalX = 0
    GoalY = 0
    dimX = 0
    dimY = 0
    startX = 0
    startY = 0
    OBS_X = []
    OBS_Y = []

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
            if self.direction == G.SOUTH:
                self.robotX += 1
            elif self.direction == G.EAST:
                self.robotY += 1;
            elif self.direction == G.NORTH:
                self.robotX -= 1;
            elif self.direction == G.WEST:
                self.robotY -= 1
            s += "<<<<SCRIPT," + "bot.move_forward({})\n".format(MOVE_POWER)
            time = self.calcTravelTime(1, MOVE_POWER)
            s += "bot.wait({})\n".format(time) + ">>>>\n"
        if code == "Backward":
            if self.direction == G.SOUTH:
                self.robotX -= 1
            elif self.direction == G.EAST:
                self.robotY -= 1;
            elif self.direction == G.NORTH:
                self.robotX += 1;
            elif self.direction == G.WEST:
                self.robotY += 1
            s += "<<<<SCRIPT," + "bot.move_backward({})\n".format(MOVE_POWER)
            time = self.calcTravelTime(1, MOVE_POWER)
            s += "bot.wait({})\n".format(time) + ">>>>\n"
        if code == "TurnLeft":
            self.direction = (self.direction + 1) % 4
            s += "<<<<SCRIPT," + "bot.move_counter_clockwise({})\n".format(TURN_POWER)
            s += "bot.wait({})\n".format(TURN_TIME) + ">>>>\n"
        if code == "TurnRight":
            self.direction = (self.direction + 3) % 4
            s += "<<<<SCRIPT," + "bot.move_clockwise({})\n".format(TURN_POWER)
            s += "bot.wait({})\n".format(TURN_TIME) + ">>>>\n"
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

    # checks whether the current position of the robot is on an obstacle in the map/maze
    # returns True if the robot is on an obstacle, and False if it is not.
    def check_obstacles(self):
        on_obstacle = False
        possible_locations = []
        for i in range(len(self.OBS_X)):
            if self.robotX == self.OBS_X[i]:
                possible_locations.append(i)
        for j in range(len(possible_locations)):
            if self.robotY == self.OBS_Y[possible_locations[j]]:
                on_obstacle = True
        return on_obstacle

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
                if self.check_obstacles():
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
        if self.direction == G.NORTH:
            return ""
        elif self.direction == G.SOUTH:
            return "TurnRight\nTurnRight\n"
        elif self.direction == G.EAST:
            return "TurnLeft\n"
        elif self.direction == G.WEST:
            return "TurnRight\n"

    # executing specifically reset()
    def rerun(self, code):
        s = ""
        list = code.split("\n")
        length = len(list)
        for i in range(0, length):
            code = list[i]
            temp, goal = self.moveRobot(code)
            if temp != "":
                s += temp
            print temp
            # time.sleep(1)
        return s

    # reverts direction back to starting direction, starting at direction NORTH
    def revert_dir(self, dir):
        # assuming everything starts facing NORTH
        if dir == G.NORTH:
            return ""
        elif dir == G.SOUTH:
            return "TurnRight\nTurnRight\n"
        elif dir == G.EAST:
            return "TurnRight\n"
        else:
            return "TurnLeft\n"

    # returns the string to send to minibot for it to revert to its starting point
    def reset(self):
        distX = self.robotX - self.startX
        distY = self.robotY - self.startY
        s = ""
        if distX == 0 and distY == 0:
            return
        if distX > 0:
            # go north
            s += self.check_dir()
            for i in range(distX):
                s += "Forward\n"
            s += self.revert_dir(self.start_dir)
        elif distX < 0:
            # go south
            s += self.check_dir()
            for i in range(distX):
                s += "Backward\n"
            s += self.revert_dir(self.start_dir)
        if distY > 0:
            # go west
            s += self.check_dir() + "TurnLeft\n"
            for i in range(distY):
                s += "Forward\n"
            s += "TurnRight\n"
            s += self.revert_dir(self.start_dir)
        elif distY < 0:
            # go east
            s += self.check_dir() + "TurnRight\n"
            for i in range(distY):
                s += "Forward\n"
            s += "TurnLeft\n"
            s += self.revert_dir(self.start_dir)
        self.rerun(s)

    # checks whether goal is reached by comparing goal to current location
    # used in GUI
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
