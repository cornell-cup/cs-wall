# main function that receives the string of inputCode to output minibot movement
def runCode(inputCode):
    # split the code by lines
    words = inputCode.split("\n")

    # for each word in the line:
    for word in words:
        # print the word
        print(word)

    from collections import defaultdict
    VariableMap = defaultdict(list)
    VariableMap['a'].append(1)
    VariableMap['b'].append(2)
    VariableMap['c'].append(3)

# function that receives the string of value to output value based on the variable map
def parseValue(s):
#     int left, right;
#     if (s.contains("+")) {
#     String[] temp = s.split("\\+");
#     if (VariableMap.containsKey(temp[0])) {
#     left = VariableMap.get(temp[0]);
#     } else {
#     left = Integer.parseInt(temp[0]);
#     }
#     if (VariableMap.containsKey(temp[1])) {
#     right = VariableMap.get(temp[1]);
#     } else {
#     right = Integer.parseInt(temp[1]);
#     }
#     return left + right;
#     } else if (s.contains("-")) {
#     String[]
#     temp = s.split("\\-");
#     if (VariableMap.containsKey(temp[0])) {
#     left = VariableMap.get(temp[0]);
#     } else {
#     left = Integer.parseInt(temp[0]);
#     }
#     if (VariableMap.containsKey(temp[1])) {
#     right = VariableMap.get(temp[1]);
#     } else {
#     right = Integer.parseInt(temp[1]);
#     }
#     return left - right;
#
# } else if (s.contains("*")) {
# String[]
# temp = s.split("\\*");
# if (VariableMap.containsKey(temp[0])) {
# left = VariableMap.get(temp[0]);
# } else {
# left = Integer.parseInt(temp[0]);
# }
# if (VariableMap.containsKey(temp[1])) {
# right = VariableMap.get(temp[1]);
# } else {
# right = Integer.parseInt(temp[1]);
# }
# return left * right;
# } else if (s.contains("/")) {
# String[]
# temp = s.split("\\/");
# if (VariableMap.containsKey(temp[0])) {
# left = VariableMap.get(temp[0]);
# } else {
# left = Integer.parseInt(temp[0]);
# }
# if (VariableMap.containsKey(temp[1])) {
# right = VariableMap.get(temp[1]);
# } else {
# right = Integer.parseInt(temp[1]);
# }
# return left / right;
# }
# // only
# one
# symbol or value
# if (VariableMap.containsKey(s))
# {
# return VariableMap.get(s);
# } else {
# return Integer.parseInt(s);
# }
    return 0;

# function that receives the string of code to output minibot movement
# the input in the code contains Forward, Backward, TurnLeft, TurnRight
def moveRobot(code):
    return 0;

runCode("Forward\nForward\nForward")