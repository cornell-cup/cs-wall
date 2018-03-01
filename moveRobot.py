# this function is designed to receive movement blocks of Forward, Backward
# TurnLeft, TurnRight and prints corresponding Minibot API
# <<<<SCRIPT,(code)>>>>
def moveRobot(code):
    direction = 0
    robotX = 0
    robotY = 0
    if code == "Forward":
        if direction == 0:
           robotY += 1
        elif direction == 1:
            robotX += 1;
        elif direction == 2:
          robotY -= 1;
        elif direction == 3:
            robotX -= 1
    if code == "Backward":
        if direction == 0:
           robotY -= 1
        elif direction == 1:
            robotX -= 1;
        elif direction == 2:
          robotY += 1;
        elif direction == 3:
            robotX += 1

    if code == "TurnLeft":
        direction = (direction + 1) % 4
    if code == "TurnRight":
        direction = (direction + 3) % 4
