import time
import Globals as G
import a4988


class SystemControl:
    """Receives the translated RFID's from Wall through Parser and calls the 2D system movements accordingly.
    In addition, records the current position of the bot during its movement as class variables. """

    reset_flag = False
    start_dir = 1
    direction = start_dir
    startX = 3
    startY = 1
    robotX = startX
    robotY = startY
    GoalX = 3
    GoalY = 4
    dimX = 5
    dimY = 5
    OBS_X = []
    OBS_Y = []

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
        on_obstacle = False
        if code == "Forward":
            if self.direction == G.SOUTH:
                self.robotX += 1
            elif self.direction == G.EAST:
                self.robotY += 1;
            elif self.direction == G.NORTH:
                self.robotX -= 1;
            elif self.direction == G.WEST:
                self.robotY -= 1
            if self.checkBounds():
                out = True
                return goal_reached, out, on_obstacle
            if self.check_obstacles():
                on_obstacle = True
                return goal_reached, out, on_obstacle
            self.moveForward()
        if code == "Backward":
            if self.direction == G.SOUTH:
                self.robotX -= 1
            elif self.direction == G.EAST:
                self.robotY -= 1;
            elif self.direction == G.NORTH:
                self.robotX += 1;
            elif self.direction == G.WEST:
                self.robotY += 1
            if self.checkBounds():
                out = True
                return goal_reached, out, on_obstacle
            if self.check_obstacles():
                on_obstacle = True
                return goal_reached, out, on_obstacle
            self.moveBackward()
        if code == "TurnLeft":
            self.direction = (self.direction + 1) % 4
            self.turnLeft()
        if code == "TurnRight":
            self.direction = (self.direction + 3) % 4
            self.turnRight()
        if self.robotX == self.GoalX and self.robotY == self.GoalY:
            goal_reached = True
        return goal_reached, out, on_obstacle

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

    # executing specifically reset()
    def rerun(self, code):
        action_list = code.split("\n")
        length = len(action_list)
        for i in range(0, length-1):
            code = action_list[i]
            self.moveRobot(code)
            print("robotX")
            print(self.robotX)
            print("robotY")
            print(self.robotY)
            print(self.reset_flag)
            # TODO sleep time probably needs to correlate to 2D system move time.
            time.sleep(2)

    # runs the actions on the 2D system
    def run(self, code):
        action_list = code.split("\n")
        length = len(action_list)
        goal = False
        for i in range(0, length-1):
            code = action_list[i]
            goal, out, on_obstacle = self.moveRobot(code)
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
            if on_obstacle:
                print("INVALID, ON OBSTACLE")
                return False
            if self.reset_flag:
                print("RESET")
                return False
        return goal

    # below are methods from the ECE team
    def moveForward(self):
        # motor
        if self.direction == 0:
            a4988.moveVerticalDown(1000)
        elif self.direction == 1:
            a4988.moveHorizontalUp(1000)
        elif self.direction == 2:
            a4988.moveVerticalUp(1000)
        else:
            a4988.moveHorizontalDown(1000)

    def moveBackward(self):
        # motor
        if self.direction == 0:
            a4988.moveVerticalUp(1000)
        elif self.direction == 1:
            a4988.moveHorizontalDown(1000)
        elif self.direction == 2:
            a4988.moveVerticalDown(1000)
        else:
            a4988.moveHorizontalUp(1000)

    def turnRight(self):
        # motor
        # TODO move servo
        print "turnRight"

    def turnLeft(self):
        # motor
        # TODO move servo
        print "turnLeft"
