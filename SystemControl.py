import time
import Globals as G
#import a4988

class SystemControl:
    """Receives the translated RFID's from Wall through Parser and calls the 2D system movements accordingly.
    In addition, records the current position of the bot during its movement as class variables. """

    reset_flag = False
    time_step = 0
    start_dir = 1
    direction = start_dir
    startX = 3
    startY = 1
    robotX = startX
    robotY = startY
    GoalX = 3
    GoalY = 4
    dimX = 5
    OBS = []
    dead_pirates = []
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
            check, obs = self.check_obstacles(self.robotX, self.robotY)
            if self.checkBounds(self.robotX, self.robotY):
                out = True
                return goal_reached, out, on_obstacle
            if check:
                on_obstacle = True
                return goal_reached, out, on_obstacle
            # a4988.moveVerticalUp(10)
        if code == "Backward":
            if self.direction == G.SOUTH:
                self.robotX -= 1
            elif self.direction == G.EAST:
                self.robotY -= 1
            elif self.direction == G.NORTH:
                self.robotX += 1
            elif self.direction == G.WEST:
                self.robotY += 1
            check, obs = self.check_obstacles(self.robotX, self.robotY)
            if self.checkBounds(self.robotX, self.robotY):
                out = True
                return goal_reached, out, on_obstacle
            if check:
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
                check, obs = self.check_obstacles(x, y)
                if self.checkBounds(x, y):
                    # if a possible block is out of bounds, then the following blocks in the same direction will also
                    # be out of bounds, so no need to continue checking.
                    break
                elif check:
                    self.OBS.remove(obs)
                    self.dead_pirates = []
                    self.dead_pirates.append([x, y])
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
            for i in range(-distX):
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
            for i in range(-distY):
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
        if y >= self.dimX:
            out_of_bounds = True
            y = self.dimX - 1
        elif y < 0:
            out_of_bounds = True
            y = 0
        return out_of_bounds

    def check_obstacles(self, x, y):
        """checks whether the current position of the robot is on an obstacle in the map/maze
        returns True if the robot is on an obstacle, and False if it is not."""
        for i in range(len(self.OBS)):
            temp = self.OBS[i]
            if temp.location[0] == x and temp.location[1] == y:
                return True, temp
        return False, None

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
            # TODO sleep time probably needs to correlate to 2D system move time.
            time.sleep(2)

    def run(self, code, obs, ded_obs):
        """runs the actions on the 2D system"""
        action_list = code.split("\n")
        length = len(action_list)
        goal = False
        for i in range(0, length-1):
            code = action_list[i]
            self.time_step += 1
            self.move_obs()
            goal, out, on_obstacle = self.moveRobot(code)
            print("robotX")
            print(self.robotX)
            print("robotY")
            print(self.robotY)
            obs = self.OBS
            if not len(self.dead_pirates) == 0:
                ded_obs.append(self.dead_pirates[0])
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

    def move_obs(self):
        """Moves the obstacles according to designated path"""
        for i in range(len(self.OBS)):
            temp_obs = self.OBS[i]
            if not temp_obs.movable:
                continue
            path = temp_obs.path
            movement_serial = self.time_step % len(path)
            self.OBS[i].location = path[movement_serial]

    # def check_random(self, pseudo_x, pseudo_y):
    #     """checks whether a single random move of the robot is feasible, ie not out of bounds and not overlapping"""
    #     # check whether it is out of bounds or overlapping with another obstacle, which are not allowed
    #     allowed = False
    #     if pseudo_x < 0 or pseudo_y < 0 or pseudo_x >= self.dimX or pseudo_y >= self.dimX:
    #         # check if it is out of bounds
    #         return allowed
    #     else:
    #         # check if it is overlapping with the obstacles
    #         for i in range(len(self.OBS)):
    #             temp = self.OBS[i]
    #             if temp.location[0] == [pseudo_x] and temp.location[1] == [pseudo_y]:
    #                 return False
    #         allowed = True
    #     return allowed
    #
    # def move_obs_random(self):
    #     """moves the obstacle randomly"""
    #     # possible movements: north, south, east, west, attack
    #     for i in range(len(self.OBS)):
    #         if not self.OBS[i].movable:
    #             continue
    #         allowed = False
    #         while not allowed:
    #             index = randint(1, 4)
    #             if index == 1:
    #                 # move north
    #                 temp_x = self.OBS[i].location[0] - 1
    #                 temp_y = self.OBS[i].location[1]
    #                 if self.check_random(temp_x, temp_y):
    #                     self.OBS[i].location[0] = temp_x
    #                     allowed = True
    #             elif index == 2:
    #                 # move south
    #                 temp_x = self.OBS[i].location[0] + 1
    #                 temp_y = self.OBS[i].location[1]
    #                 if self.check_random(temp_x, temp_y):
    #                     self.OBS[i].location[0] = temp_x
    #                     allowed = True
    #             elif index == 3:
    #                 # move east
    #                 temp_x = self.OBS[i].location[0]
    #                 temp_y = self.OBS[i].location[1] + 1
    #                 if self.check_random(temp_x, temp_y):
    #                     self.OBS[i].location[1] = temp_y
    #                     allowed = True
    #             elif index == 4:
    #                 # move west
    #                 temp_x = self.OBS[i].location[0]
    #                 temp_y = self.OBS[i].location[1] - 1
    #                 if self.check_random(temp_x, temp_y):
    #                     self.OBS[i].location[1] = temp_y
    #                     allowed = True
