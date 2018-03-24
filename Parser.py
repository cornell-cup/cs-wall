from collections import defaultdict

class Parser:
    # class parser is used to parse the block code into robot command

    VariableMap = defaultdict(list)
    robotX = 0
    robotY = 0
    result = ""

    def __init__(self):
        """initialize the location of the robot and the variable map in the map"""
        self.VariableMap = defaultdict(list)
        self.robotX = 0
        self.robotY = 0
        self.result = ""

    def translateRFID(self, rfidfile):
        """translate the RFID file to the blocks"""

        # open file with list of RFIDs and another file of RFID tag's corresponding
        # blocks and translate the file from RFID tags into block language
        file1 = open(rfidfile, "r")
        file2 = open("input/codeBlock.txt", "r")
        blockmap = {}
        st = file2.readline()
        # open file of RFID tag's corresponding blocks record and store them in a blockmap
        while st:
            key, value = st.replace("\n", "").split(" ")
            blockmap.setdefault(key, value)
            st = file2.readline()
        file2.close()
        result = ""
        rfids = file1.readline()
        # open file of RFID tag and use the blockmap to translate it to block syntax
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

    def innerInt(self, s):
        """turn a string containing integer to int, return 0 if error occurred"""
        try:
            int(s)
            return int(s)
        except ValueError:
            return 0

    def parseValue(self, s):
        """receives the string of value to output value based on the variable map"""
        if "+" in s:
            # encounter +, combine value on the left and right
            temp = s.split("+")
            # parse left statement's value
            if temp[0] in self.VariableMap:
                left = self.VariableMap.get(temp[0])
            else:
                left = self.innerInt(temp[0])
            # parse right statement's value
            if temp[1] in self.VariableMap:
                right = self.VariableMap.get(temp[1])
            else:
                right = self.innerInt(temp[1])
            return left+right
        elif "-" in s:
            # encounter -, subtract value on the left with value on the right
            temp = s.split("-")
            if temp[0] in self.VariableMap:
                left = self.VariableMap.get(temp[0])
            else:
                left = self.innerInt(temp[0])
            if temp[1] in self.VariableMap:
                right = self.VariableMap.get(temp[1])
            else:
                right = self.innerInt(temp[1])
            return left - right
        elif "*" in s:
            # encounter *, multiply value on the left and right
            temp = s.split("*")
            if temp[0] in self.VariableMap:
                left = self.VariableMap.get(temp[0])
            else:
                left = self.innerInt(temp[0])
            if temp[1] in self.VariableMap:
                right = self.VariableMap.get(temp[1])
            else:
                right = self.innerInt(temp[1])
            return left * right
        elif "/" in s:
            # encounter /, divide value on the left with value on the right
            temp = s.split("/")
            if temp[0] in self.VariableMap:
                left = self.VariableMap.get(temp[0])
            else:
                left = self.innerInt(temp[0])
            if temp[1] in self.VariableMap:
                right = self.VariableMap.get(temp[1])
            else:
                right = self.innerInt(temp[1])
            return left / right
        # s is a value corresponding to an element in VariableMap
        if s in self.VariableMap:
            return self.VariableMap.get(s)
        else:
            # s is just a int value
            self.innerInt(s)


    def runCode(self, inputCode):
        """main function that receives the string of inputCode to output minibot movement"""

        # split the code by lines
        codeLines = inputCode.split("\n")
        movement = ['Forward', 'Backward', 'TurnLeft', 'TurnRight']
        while len(codeLines) > 0:
            code = codeLines.pop(0)
            # the code starts with movement statement
            if code in movement:
                self.result += code+"\n"
                continue
            # the code starts with FOR statement
            if code.split(" ")[0] == "FOR":
                ForCode = ""
                temp = codeLines.pop(0)
                # record code in FOR loop until END statement
                while temp != "END":
                    ForCode += temp + "\n"
                    temp = codeLines.pop(0)
                loopNum = int(code.split(" ")[1].split("x")[0]);
                for i in range(0, loopNum) :
                    self.runCode(ForCode)
                continue
            # the code starts with SET statement
            if code.split(" ")[0] == "SET":
                # find first and second statement in SET
                one, two = code[4:].split("=")
                # replace first statement's value in Variable Map to the value evaluated by second statement
                self.VariableMap[one.replace(" ", "")] = self.parseValue(two.replace(" ", ""))
                continue
            # the code starts with IF statement
            if code.split(" ")[0] == "IF":
                logic = code[3:code.find("DO")].replace(" ", "")
                IfCode = ""
                temp = codeLines.pop(0)
                # record code in IF clause until END statement
                while temp != "END":
                    IfCode += temp + "\n"
                    temp = codeLines.pop(0)
                if self.parseLogic(logic):
                    self.runCode(IfCode)
                continue
            # the code starts with WHILE statement
            if code.split(" ")[0] == "WHILE":
                logic = code[6:code.find("DO")].replace(" ", "")
                WhileCode = ""
                temp = codeLines.pop(0)
                # record code in WHILE loop until END statement
                while temp != "END":
                    WhileCode += temp + "\n"
                    temp = codeLines.pop(0)
                while self.parseLogic(logic):
                    self.runCode(WhileCode)
                continue
        return self.result

    def parseLogic(self, s):
        """receives the string s and output value it corresponding to"""

        if "Destination" in s:
            s.split("Destination")
            return self.robotX != 3 & self.robotY != 3
        elif ">" in s:
            # logic is >
            temp = s.split(">")
            return self.parseValue(temp[0]) > self.parseValue(temp[1])
        elif "<" in s:
            # logic is <
            temp = s.split("<")
            return self.parseValue(temp[0]) < self.parseValue(temp[1])
        elif "=" in s:
            # logic is =
            temp = s.split("=")
            return self.parseValue(temp[0]) == self.parseValue(temp[1])
        else:
            return False

    # function that
    def moveRobot(self, code):
        """receives the string of code to output minibot movement
        the input in the code contains Forward, Backward, TurnLeft, TurnRight"""
        print(code)
        return 0


# p = Parser()
# print (p.parseValue("1+2a"))
# print p.runCode(p.translateRFID("rfidFOR.txt"))
