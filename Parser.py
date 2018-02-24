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
        result += (blockmap.get(rfids) + "\n")
        rfids = file1.readline()
    file1.close()
    # ask: what does this method return? A string block?
    return result



# Note: the field variablemap should be changed to whatever the field is named in parser
VariableMap = {}

# function that receives the string of value to output value based on the variable map
def parseValue(s):
    left, right = 0;
    if "+" in s:
        temp = s.split("\\+")
        if temp[0] in VariableMap.keys():
            left = VariableMap.get(temp[0])
        else:
            left = int(temp[0])
        if temp[1] in VariableMap.keys():
            right = VariableMap.get(temp[1])
        else:
            right = int(temp[1])
        return left+right
    elif "-" in s:
        temp = s.split("\\-")
        if temp[0] in VariableMap.keys():
            left = VariableMap.get(temp[0])
        else:
            left = int(temp[0])
        if temp[1] in VariableMap.keys():
            right = VariableMap.get(temp[1])
        else:
            right = int(temp[1])
        return left - right
    elif "*" in s:
        temp = s.split("\\*")
        if temp[0] in VariableMap.keys():
            left = VariableMap.get(temp[0])
        else:
            left = int(temp[0])
        if temp[1] in VariableMap.keys():
            right = VariableMap.get(temp[1])
        else:
            right = int(temp[1])
        return left * right
    elif "/" in s:
        temp = s.split("\\/")
        if temp[0] in VariableMap.keys():
            left = VariableMap.get(temp[0])
        else:
            left = int(temp[0])
        if temp[1] in VariableMap.keys():
            right = VariableMap.get(temp[1])
        else:
            right = int(temp[1])
        return left / right
    if s in VariableMap.keys():
        return VariableMap.get(s)
    else:
        return int(s)


# main function that receives the string of inputCode to output minibot movement
def runCode(inputCode):
    # split the code by lines
    codeLines = inputCode.split("\n")
    movement = ['Forward', 'Backward', 'TurnLeft', 'TurnRight']

    from collections import defaultdict
    VariableMap = defaultdict(list)
    VariableMap['a'].append(1)
    VariableMap['b'].append(2)
    VariableMap['c'].append(3)

    while len(codeLines) > 0:
        code = codeLines.pop(0)
        if code in movement:
            moveRobot(code)
            continue
        if code.split(" ")[0] == "FOR":
            ForCode = ""
            temp = codeLines.remove(0)
            while temp != "END":
                ForCode += temp + "\n"
                temp = codeLines.remove(0)
            loopNum = int(code.split(" ")[1].split("x")[0]);
            for i in range(0, loopNum) :
                runCode(ForCode)
            continue
        if code.split(" ")[0] == "SET":
            # TODO
            VariableMap[code.substring(4, code.length()).split("=")[0].replace(" ", "")].append(
                            parseValue(code.split("=")[1].replace(" ", "")))
            continue
        if code.split(" ")[0] == "IF":
            logic = code.substring(3, code.length()).replace(" ", "");
            IfCode = ""
            temp = codeLines.remove(0)
            while temp != "END":
                IfCode += temp + "\n";
                temp = codeLines.remove(0);
            if parseLogic(logic):
                runCode(IfCode);
            continue;
        if code.split(" ")[0] == "WHILE":
            logic = code.substring(6, code.indexOf("DO")).replace(" ", "");
            WhileCode = "";
            temp = codeLines.remove(0);
            while temp!= "END":
                WhileCode += temp + "\n";
                temp = codeLines.remove(0);
            while parseLogic(logic):
                runCode(WhileCode);
            continue;

# function that receives the string s and output value it corresponding to
def parseLogic(s):
    robotX = 0
    robotY = 0
    if s.contains("Destination"):
        s.split("Destination");
        return robotX != 3 & robotY != 3
    elif s.contains(">"):
        temp = s.split(">");
        return parseValue(temp[0]) > parseValue(temp[1])
    elif s.contains("<"):
        temp = s.split("<");
        return parseValue(temp[0]) < parseValue(temp[1])
    elif s.contains("="):
        temp = s.split("=")
        return parseValue(temp[0]) == parseValue(temp[1])
    else:
        return False


# function that receives the string of code to output minibot movement
# the input in the code contains Forward, Backward, TurnLeft, TurnRight
def moveRobot(code):
    print code
    return 0

runCode(translateRFID("rfid.txt"))