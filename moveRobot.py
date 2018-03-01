# this function is designed to receive movement blocks of Forward, Backward
# TurnLeft, TurnRight and prints corresponding Minibot API
# returns: <<<<SCRIPT,(code)>>>>, a String
# Also note, I don't think that there are parentheses around the code according to their parser
# Also, note that "dummy" will be changed
# Question: do we need to move this on our grid? i.e. do we need the variables direction, robotX, and robotY?


def moveRobot(code):
    s = "<<<<SCRIPT,"
    # direction = 0
    # robotX = 0
    # robotY = 0
    if code == "Forward":
        # if direction == 0:
        #    robotY += 1
        # elif direction == 1:
        #     robotX += 1;
        # elif direction == 2:
        #   robotY -= 1;
        # elif direction == 3:
        #     robotX -= 1
        power = "dummy"
        s += "move_forward(" + power + ")\n"
    if code == "Backward":
        # if direction == 0:
        #    robotY -= 1
        # elif direction == 1:
        #     robotX -= 1;
        # elif direction == 2:
        #   robotY += 1;
        # elif direction == 3:
        #     robotX += 1
        power = "dummy"
        s += "move_backward(" + power + ")\n"
    if code == "TurnLeft":
        # direction = (direction + 1) % 4
        power = "dummy"
        s += "move_counter_clockwise(" + power + ")\n"
    if code == "TurnRight":
        # direction = (direction + 3) % 4
        power = "dummy"
        s += "move_clockwise(" + power + ")\n"

    s += ">>>>"
    return s
