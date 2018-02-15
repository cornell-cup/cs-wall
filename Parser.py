# function to translate the RFID file to the blocks
def translateRFID(RFIDfile):
    # String inputCode = "";
    # File codeFile = new File("rfid.txt");
    # File codeBlockFile = new
    # File("codeBlock.txt");
    # BufferedReader
    # br = null, br2 = null;
    # try {
    # br = new BufferedReader(new FileReader(codeFile));
    # br2 = new BufferedReader(new FileReader(codeBlockFile));
    # } catch (FileNotFoundException e1) {
    # e1.printStackTrace();
    # }
    #
    # // connect rfid code to actual for while code block
    # HashMap < String, String > codeBlock = new HashMap < String, String > ();
    #
    # String
    # st;
    # try {
    # while ((st = br2.readLine()) != null){
    # codeBlock.put(st.split(" ")[0], st.split(" ")[1]);
    # }
    # } catch(IOException
    # e1) {
    # e1.printStackTrace();

}
    return 0;

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