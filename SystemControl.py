import time


class SystemControl:

    SOUTH = 0
    EAST = 1
    NORTH = 2
    WEST = 3
    reset_flag = False
    direction = 1
    startX = 3
    startY = 1
    robotX = startX
    robotY = startY
    GoalX = 3
    GoalY = 4
    dimX = 5
    dimY = 5

    def __init__(self):
        self.direction = 1
        self.startX = 3
        self.startY = 1
        self.robotX = self.startX
        self.robotY = self.startY
        self.GoalX = 3
        self.GoalY = 4
        self.dimX = 5
        self.dimY = 5

    # returns one line of the SCRIPT string and a boolean representing whether the target goal is reached
    def moveRobot(self, code):
        goal_reached = False
        out = False
        if code == "Forward":
            if self.direction == self.SOUTH:
                self.robotX += 1
            elif self.direction == self.EAST:
                self.robotY += 1;
            elif self.direction == self.NORTH:
                self.robotX -= 1;
            elif self.direction == self.WEST:
                self.robotY -= 1
            if self.checkBounds():
                out = True
                goal_reached = False
                return goal_reached, out
            # TODO method moveForward
        if code == "Backward":
            if self.direction == self.SOUTH:
                self.robotX -= 1
            elif self.direction == self.EAST:
                self.robotY -= 1;
            elif self.direction == self.NORTH:
                self.robotX += 1;
            elif self.direction == self.WEST:
                self.robotY += 1
            if self.checkBounds():
                out = True
                goal_reached = False
                return goal_reached, out
            # TODO method moveBackward
        if code == "TurnLeft":
            self.direction = (self.direction + 1) % 4
            # TODO method turnLeft
        if code == "TurnRight":
            self.direction = (self.direction + 3) % 4
            # TODO method turnRight
        if self.robotX == self.GoalX and self.robotY == self.GoalY:
            goal_reached = True
        return goal_reached, out

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

    # returns the robot from its current location to the starting point
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
        elif distX < 0:
            # go south
            s += self.check_dir()
            for i in range(distX):
                s += "Backward\n"
        if distY > 0:
            # go west
            s += self.check_dir() + "TurnLeft\n"
            for i in range(distY):
                s += "Forward\n"
        elif distY < 0:
            # go east
            s += self.check_dir() + "TurnRight\n"
            for i in range(distY):
                s += "Forward\n"
        self.rerun(s)

    # checks whether the current position of the robot is out of bounds in the map/maze
    # if the robot is out of bounds, then it resets the position of the robot at its last position in bound
    # returns True if the robot is out of bounds, and False if it is not.
    def checkBounds(self):
        out_of_bounds = False
        if self.robotX >= self.dimX:
            out_of_bounds = True
            self.robotX = self.dimX - 1
        elif self.robotX < 0:
            out_of_bounds = True
            self.robotX = 0
        if self.robotY >= self.dimY:
            out_of_bounds = True
            self.robotY = self.dimY - 1
        elif self.robotY < 0:
            out_of_bounds = True
            self.robotY = 0
        return out_of_bounds

    # executing specifically reset()
    def rerun(self, code):
        action_list = code.split("\n")
        length = len(action_list)
        goal = False
        for i in range(0, length):
            code = action_list[i]
            goal, out = self.moveRobot(code)
            print("robotX")
            print(self.robotX)
            print("robotY")
            print(self.robotY)
            print(self.reset_flag)
            # TODO sleep time probably needs to correlate to 2D system move time.
            time.sleep(2)
            if out:
                print("OUT OF BOUNDS")
                return False
        return goal

    # runs the actions on the 2D system
    def run(self, code):
        action_list = code.split("\n")
        length = len(action_list)
        goal = False
        for i in range(0, length):
            code = action_list[i]
            goal, out = self.moveRobot(code)
            print("robotX")
            print(self.robotX)
            print("robotY")
            print(self.robotY)
            print(self.reset_flag)
            # TODO sleep time probably needs to correlate to 2D system move time.
            time.sleep(2)
            if out:
                print("OUT OF BOUNDS")
                return False
            if self.reset_flag:
                print("RESET")
                return False
        return goal
