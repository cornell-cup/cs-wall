# this function is designed to receive movement blocks of Forward, Backward
# TurnLeft, TurnRight and prints corresponding Minibot API
# returns: <<<<SCRIPT,(code)>>>>, a String
# Also note, I don't think that there are parentheses around the code according to their parser
# TODO change "dummy" to actual power level
# TODO "dummy" refers to the power needed for minibot to move 1 grid length OR turn
# TODO figure out minibot's power level and whether we need to use the wait(time) function, also think about connecting
# TODO robotX robotY to an imaginary gui


def moveRobot(code):
    s = "<<<<SCRIPT,"
    # direction = 0
    # robotX = 0
    # robotY = 0
    move_lev = 50
    turn_lev = 50
    if code == "Forward":
        # if direction == 0:
        #    robotY += 1
        # elif direction == 1:
        #     robotX += 1;
        # elif direction == 2:
        #   robotY -= 1;
        # elif direction == 3:
        #     robotX -= 1
        power = str(move_lev)
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
        power = str(move_lev)
        s += "move_backward(" + power + ")\n"
    if code == "TurnLeft":
        # direction = (direction + 1) % 4
        power = str(turn_lev)
        s += "move_counter_clockwise(" + power + ")\n"
    if code == "TurnRight":
        # direction = (direction + 3) % 4
        power = str(turn_lev)
        s += "move_clockwise(" + power + ")\n"

    s += ">>>>"
    return s
