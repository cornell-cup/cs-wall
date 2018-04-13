import time
import Globals as G
# import a4988


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
    OBS = []
    attack_range = 2

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

    def moveRobot(self, code):
        """returns one line of the SCRIPT string and a boolean representing whether the target goal is reached"""
        goal_reached = False
        out = False
        on_obstacle = False
        if code == "Forward":
            if self.direction == G.SOUTH:
                self.robotX += 1
            elif self.direction == G.EAST:
                self.robotY += 1
            elif self.direction == G.NORTH:
                self.robotX -= 1
            elif self.direction == G.WEST:
                self.robotY -= 1
            if self.checkBounds(self.robotX, self.robotY):
                out = True
                return goal_reached, out, on_obstacle
            if self.check_obstacles(self.robotX, self.robotY):
                on_obstacle = True
                return goal_reached, out, on_obstacle
            # self.moveForward()
        if code == "Backward":
            if self.direction == G.SOUTH:
                self.robotX -= 1
            elif self.direction == G.EAST:
                self.robotY -= 1
            elif self.direction == G.NORTH:
                self.robotX += 1
            elif self.direction == G.WEST:
                self.robotY += 1
            if self.checkBounds(self.robotX, self.robotY):
                out = True
                return goal_reached, out, on_obstacle
            if self.check_obstacles(self.robotX, self.robotY):
                on_obstacle = True
                return goal_reached, out, on_obstacle
            # self.moveBackward()
        if code == "TurnLeft":
            self.direction = (self.direction + 1) % 4
            # self.turnLeft()
        if code == "TurnRight":
            self.direction = (self.direction + 3) % 4
            # self.turnRight()
        if code == "Attack":
            in_range = []
            if self.direction == G.SOUTH:
                for dist in range(self.attack_range):
                    in_range.append([self.robotX + (dist + 1), self.robotY])
            elif self.direction == G.NORTH:
                for dist in range(self.attack_range):
                    in_range.append([self.robotX - (dist + 1), self.robotY])
            elif self.direction == G.EAST:
                for dist in range(self.attack_range):
                    in_range.append([self.robotX, self.robotY + (dist + 1)])
            elif self.direction == G.WEST:
                for dist in range(self.attack_range):
                    in_range.append([self.robotX, self.robotY - (dist + 1)])
            for i in range(len(in_range)):
                x = in_range[i][0]
                y = in_range[i][1]
                temp_x = x
                temp_y = y
                if self.checkBounds(temp_x, temp_y):
                    # if a possible block is out of bounds, then the following blocks in the same direction will also
                    # be out of bounds, so no need to continue checking.
                    break
                elif self.check_obstacles(x, y):
                    self.OBS.remove([x, y])
                    break
        if self.robotX == self.GoalX and self.robotY == self.GoalY:
            goal_reached = True
        return goal_reached, out, on_obstacle

    def check_dir(self):
        """sets the direction to NORTh"""
        if self.direction == G.NORTH:
            return ""
        elif self.direction == G.SOUTH:
            return "TurnRight\nTurnRight\n"
        elif self.direction == G.EAST:
            return "TurnLeft\n"
        elif self.direction == G.WEST:
            return "TurnRight\n"

    def revert_dir(self, dir):
        """reverts direction back to starting direction, starting at direction NORTH"""
        # assuming everything starts facing NORTH
        if dir == G.NORTH:
            return ""
        elif dir == G.SOUTH:
            return "TurnRight\nTurnRight\n"
        elif dir == G.EAST:
            return "TurnRight\n"
        else:
            return "TurnLeft\n"

    def reset(self):
        """returns the robot from its current location to the starting point"""
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

    def checkBounds(self, x, y):
        """checks whether the current position of the robot is out of bounds in the map/maze
        if the robot is out of bounds, then it resets the position of the robot at its last position in bound
        returns True if the robot is out of bounds, and False if it is not."""
        out_of_bounds = False
        if x >= self.dimX:
            out_of_bounds = True
            x = self.dimX - 1
        elif x < 0:
            out_of_bounds = True
            x = 0
        if y >= self.dimY:
            out_of_bounds = True
            y = self.dimY - 1
        elif y < 0:
            out_of_bounds = True
            y = 0
        return out_of_bounds

    def check_obstacles(self, x, y):
        """checks whether the current position of the robot is on an obstacle in the map/maze
        returns True if the robot is on an obstacle, and False if it is not."""
        on_obstacle = False
        if [x, y] in self.OBS:
            on_obstacle = True
        return on_obstacle

    def rerun(self, code):
        """executing specifically reset()"""
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

    def run(self, code, obs):
        """runs the actions on the 2D system"""
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
            obs = self.OBS
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
    # def moveForward(self):
    #     # motor
    #     if self.direction == 0:
    #         a4988.moveVerticalDown(1000)
    #     elif self.direction == 1:
    #         a4988.moveHorizontalUp(1000)
    #     elif self.direction == 2:
    #         a4988.moveVerticalUp(1000)
    #     else:
    #         a4988.moveHorizontalDown(1000)
    #
    # def moveBackward(self):
    #     # motor
    #     if self.direction == 0:
    #         a4988.moveVerticalUp(1000)
    #     elif self.direction == 1:
    #         a4988.moveHorizontalDown(1000)
    #     elif self.direction == 2:
    #         a4988.moveVerticalDown(1000)
    #     else:
    #         a4988.moveHorizontalUp(1000)
    #
    # def turnRight(self):
    #     # motor
    #     # TODO move servo
    #     print "turnRight"
    #
    # def turnLeft(self):
    #     # motor
    #     # TODO move servo
    #     print "turnLeft"
