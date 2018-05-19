import Globals as G
import time


class moveRobot:
    """Packages the translated RFID's received from Wall through Parser as minibot script in the form of
    "<<<<SCRIPT, code>>>>" and sends it to minibot. In addition, records the current position of the bot during
    its movement as class variables. """

    reset_flag = False
    time_step = 0
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
    OBS = []
    dead_pirates = []
    attack_range = 2

    def __init__(self):
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
                self.robotY += 1
            elif self.direction == G.NORTH:
                self.robotX -= 1
            elif self.direction == G.WEST:
                self.robotY -= 1
            s += "<<<<SCRIPT," + "bot.move_forward({})\n".format(MOVE_POWER)
            time = self.calcTravelTime(1, MOVE_POWER)
            s += "bot.wait({})\n".format(time) + ">>>>\n"
        if code == "Backward":
            if self.direction == G.SOUTH:
                self.robotX -= 1
            elif self.direction == G.EAST:
                self.robotY -= 1
            elif self.direction == G.NORTH:
                self.robotX += 1
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
                    # TODO does "attack" translate to minibot movement???
                    break
        if self.robotX == self.GoalX and self.robotY == self.GoalY:
            goal_reached = True
            # print("HERE"+s)
        return s, goal_reached

    def checkBounds(self, x, y):
        """checks whether the current position of the robot is out of bounds in the map/maze
        if the robot is out of bounds, then it resets the position of the robot at its last position in bound
        returns True if the robot is out of bounds, and False if it is not."""
        out_of_bounds = False
        if x >= self.dimX:
            out_of_bounds = True
            x = self.dimX-1
        elif x < 0:
            out_of_bounds = True
            x = 0
        if y >= self.dimY:
            out_of_bounds = True
            y = self.dimY-1
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

    def run(self, code, obs, ded_obs):
        """returns the finalized SCRIPT string to send to minibot"""
        s = ""
        list = code.split("\n")
        length = len(list)
        for i in range(0, length):
            if not self.reset_flag:
                code = list[i]
                self.time_step += 1
                self.move_obs()
                temp, goal = self.moveRobot(code)
                if not len(self.dead_pirates) == 0:
                    ded_obs.append(self.dead_pirates[0])
                obs = self.OBS
                if self.checkBounds(self.robotX, self.robotY):
                    break
                obs1, obs2 = self.check_obstacles(self.robotX, self.robotY)
                if obs1:
                    break
                if temp != "":
                    s += temp
                print temp
                time.sleep(1)
            else:
                s += self.reset()
                break
        return s

    def check_dir(self):
        """sets the direction to NORTH"""
        if self.direction == G.NORTH:
            return ""
        elif self.direction == G.SOUTH:
            return "TurnRight\nTurnRight\n"
        elif self.direction == G.EAST:
            return "TurnLeft\n"
        elif self.direction == G.WEST:
            return "TurnRight\n"

    def rerun(self, code):
        """executing specifically reset()"""
        s = ""
        list = code.split("\n")
        length = len(list)
        for i in range(0, length):
            code = list[i]
            temp, goal = self.moveRobot(code)
            if temp != "":
                s += temp
            # time.sleep(1)
        return s

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
        """returns the string to send to minibot for it to revert to its starting point"""
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
        return self.rerun(s)

    def move_obs(self):
        """Moves the obstacles according to designated path"""
        for i in range(len(self.OBS)):
            temp_obs = self.OBS[i]
            if not temp_obs.movable:
                continue
            path = temp_obs.path
            movement_serial = self.time_step % len(path)
            self.OBS[i].location = path[movement_serial]

    def check_goal(self):
        """checks whether goal is reached by comparing goal to current location. (used in GUI)"""
        if self.robotX == self.GoalX and self.robotY == self.GoalY:
            return True
        return False

    def calcTravelTime(self, distance, power):
        """Returns the amount of [time] Minibot needs to move to go one unit of [distance]"""
        time = 2

        # TODO Calculate travel time based off wheels of Minibot
        return time


# p = Parser()
# codeblock = p.runCode(p.translateRFID("rfidFOR.txt"))
# mr = moveRobot()
# print mr.run(codeblock)
