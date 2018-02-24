from collections import defaultdict
global VariableMap
VariableMap = defaultdict(list)
global robotX
robotX = 0
global robotY
robotY = 0

# function to translate the RFID file to the blocks
def translateRFID(rfidfile):
    file1 = open(rfidfile, "r")
    file2 = open("codeBlock.txt", "r")
    blockmap = {}
    st = file2.readline()
    while st:
        key, value = st.replace("\n", "").split(" ")
        blockmap.setdefault(key, value)
        st = file2.readline()
    file2.close()
    result = ""
    rfids = file1.readline()
    while rfids:
        rfids = rfids.replace("\n", "")
        if blockmap.get(rfids) in ['FOR', 'SET', 'IF', 'WHILE', 'END', 'Forward', 'Backward', 'TurnLeft', 'TurnRight']:
            result += "\n"
        if blockmap.get(rfids) in ['DO']:
            result += " "
        result += blockmap.get(rfids)
        if blockmap.get(rfids) in ['FOR', 'SET', 'IF', 'WHILE']:
            result += " "
        rfids = file1.readline()
    file1.close()
    return result


# function that receives the string of value to output value based on the variable map
def parseValue(s):
    global VariableMap
    if "+" in s:
        temp = s.split("+")
        if temp[0] in VariableMap:
            left = VariableMap.get(temp[0])
        else:
            left = int(temp[0])
        if temp[1] in VariableMap:
            right = VariableMap.get(temp[1])
        else:
            right = int(temp[1])
        return left+right
    elif "-" in s:
        temp = s.split("-")
        if temp[0] in VariableMap:
            left = VariableMap.get(temp[0])
        else:
            left = int(temp[0])
        if temp[1] in VariableMap:
            right = VariableMap.get(temp[1])
        else:
            right = int(temp[1])
        return left - right
    elif "*" in s:
        temp = s.split("*")
        if temp[0] in VariableMap:
            left = VariableMap.get(temp[0])
        else:
            left = int(temp[0])
        if temp[1] in VariableMap:
            right = VariableMap.get(temp[1])
        else:
            right = int(temp[1])
        return left * right
    elif "/" in s:
        temp = s.split("/")
        if temp[0] in VariableMap:
            left = VariableMap.get(temp[0])
        else:
            left = int(temp[0])
        if temp[1] in VariableMap:
            right = VariableMap.get(temp[1])
        else:
            right = int(temp[1])
        return left / right
    if s in VariableMap:
        return VariableMap.get(s)
    else:
        return int(s)


# main function that receives the string of inputCode to output minibot movement
def runCode(inputCode):
    # split the code by lines
    codeLines = inputCode.split("\n")
    movement = ['Forward', 'Backward', 'TurnLeft', 'TurnRight']
    global VariableMap

    while len(codeLines) > 0:
        code = codeLines.pop(0)
        if code in movement:
            moveRobot(code)
            continue
        if code.split(" ")[0] == "FOR":
            ForCode = ""
            temp = codeLines.pop(0)
            while temp != "END":
                ForCode += temp + "\n"
                temp = codeLines.pop(0)
            loopNum = int(code.split(" ")[1].split("x")[0]);
            for i in range(0, loopNum) :
                runCode(ForCode)
            continue
        if code.split(" ")[0] == "SET":
            one, two = code[4:].split("=")
            VariableMap[one.replace(" ", "")] = parseValue(two.replace(" ", ""))
            continue
        if code.split(" ")[0] == "IF":
            logic = code[3:code.find("DO")].replace(" ", "")
            IfCode = ""
            temp = codeLines.pop(0)
            while temp != "END":
                IfCode += temp + "\n"
                temp = codeLines.pop(0)
            if parseLogic(logic):
                runCode(IfCode)
            continue
        if code.split(" ")[0] == "WHILE":
            logic = code[6:code.find("DO")].replace(" ", "")
            WhileCode = ""
            temp = codeLines.pop(0)
            while temp != "END":
                WhileCode += temp + "\n"
                temp = codeLines.pop(0)
            while parseLogic(logic):
                runCode(WhileCode)
            continue

# function that receives the string s and output value it corresponding to
def parseLogic(s):
    if "Destination" in s:
        s.split("Destination")
        return robotX != 3 & robotY != 3
    elif ">" in s:
        temp = s.split(">")
        return parseValue(temp[0]) > parseValue(temp[1])
    elif "<" in s:
        temp = s.split("<")
        return parseValue(temp[0]) < parseValue(temp[1])
    elif "=" in s:
        temp = s.split("=")
        return parseValue(temp[0]) == parseValue(temp[1])
    else:
        return False


# function that receives the string of code to output minibot movement
# the input in the code contains Forward, Backward, TurnLeft, TurnRight
def moveRobot(code):
    print code
    return 0

runCode(translateRFID("rfidIF.txt"))