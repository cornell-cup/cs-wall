import json


class MapMaker(): 

    ###Keys to access JSON data

    #The length of one square in inches(?)
    SQUARE_UNIT = "SQUARE_UNIT"

    #Max boundaries of the map
    BOUNDARY = "BOUNDARY"
    BOUNDARY_X = "BOUNDARY_X"
    BOUNDARY_Y = "BOUNDARY_Y"
    
    #Starting position of bot
    START = "START"
    START_X = "START_X"
    START_Y = "START_Y"
    
    #Goal position of bot
    GOAL = "GOAL"
    GOAL_X = "GOAL_X"
    GOAL_Y = "GOAL_Y"

    #Impassable spots on the map
    WALLS = "WALLS"
    WALL_X = "WALL_X"
    WALL_Y = "WALL_Y"


    ###Constants to create game_data

    #game_data constants
    GAME_UNIT = "GAME_UNIT"
    GAME_START = "GAME_START"
    GAME_GOAL = "GAME_GOAL"
    GAME_MAP = "GAME_MAP"

    # Minimap space constants
    FREE_SPACE = 0
    WALL_SPACE = 1

    def __init__(self,name=None):
        #TODO: Decide if we need this field for GUI processing
        self.name = name

    def parseMap(self, file_path):
        """Returns a [game_data] from the JSON [file_path]"""

        # json_data = {}
        game_data = {}

        with open("{}.json".format(file_path),"r") as f:
            json_data = json.load(f)

            #TODO: Determine location of level files and decide if name parsing is necessary 
            #(i.e. "level_5" compared to "levels/level_5")
            self.name = file_path

            #####Interpret JSON

            ### Create map from boundaries
            # boundary = json_data.get(self.BOUNDARY,{})
            boundary = self.accessField(json_data,self.BOUNDARY)

            if not boundary:
                print("Please define a value for {}".format(self.BOUNDARY))
                return game_data

            # if not boundary:
            #     print("Boundary of map not defined")
            #     break            

            boundary_x = self.accessField(boundary,self.BOUNDARY_X)
            boundary_y = self.accessField(boundary,self.BOUNDARY_Y)

            # if ((boundary_x==None) or (boundary_y==None)):
            #     return game_data

            if boundary_x==None:
                print("Please define a valid number for {}".format(self.BOUNDARY_X))
                return game_data

            if boundary_y==None:
                print("Please define a valid number for {}".format(self.BOUNDARY_Y))
                return game_data

            miniMap = []

            for unit in range(boundary_y):
                miniMap.append([self.FREE_SPACE]*boundary_x)

            ### Add walls to map
            walls = self.accessField(json_data,self.WALLS)

            for wall in walls:
                wall_x = self.accessField(wall,self.WALL_X)
                wall_y = self.accessField(wall,self.WALL_Y)
                miniMap[wall_y][wall_x] = self.WALL_SPACE

            
            #Add map to game data
            game_data.update({self.GAME_MAP:miniMap})
            # print("Map data added")


            ### Establish starting location
            start = self.accessField(json_data,self.START)

            if not start:
                print("Please define a value for {}".format(self.START))
                return game_data

            start_x = self.accessField(start,self.START_X)
            start_y = self.accessField(start,self.START_Y)

            # if ((start_x==None) or (start_y==None)):
            #     print("Please define a value for START_X")
            #     return game_data

            if start_x==None:
                print("Please define a valid number for {}".format(self.START_X))
                return game_data

            if start_y==None:
                print("Please define a valid number for {}".format(self.START_Y))
                return game_data

            #Add map to game data
            game_data.update({self.GAME_START:(start_x,start_y)})
            # print("Start data added")


            ### Establish goal location
            goal = self.accessField(json_data,self.GOAL)

            if not goal:
                print("Please define a value for {}".format(self.GOAL))
                return game_data

            goal_x = self.accessField(goal,self.GOAL_X)
            goal_y = self.accessField(goal,self.GOAL_Y)

            # if ((goal_x==None) or (goal_y==None)):
            #     return game_data

            if goal_x==None:
                print("Please define a valid number for {}".format(self.GOAL_X))
                return game_data

            if goal_y==None:
                print("Please define a valid number for {}".format(self.GOAL_Y))
                return game_data

            #Add map to game data
            game_data.update({self.GAME_GOAL:(goal_x,goal_y)})
            # print("Goal data added")


            ### Establish unit conversion
            unit = self.accessField(json_data,self.SQUARE_UNIT)

            if unit==None:
                print("Please define a valid number for {}".format(self.SQUARE_UNIT))
                return game_data

            #Add map to game data
            game_data.update({self.GAME_UNIT:unit})
            # print("Unit data added")

        if not f:
            print("File {}.json could not be read".format(file_path))

        return game_data

    def accessField(self, dictionary,key):
        """ Accesses the [dictionary] safely with the given [key] and
            returns the corresponding value if found. If not found,
            the key is printed to the console and a None value is returned.

            This is used instead of the dictionary's get() function in order 
            to have a more controlled way to notify what is improperly defined
            in the level's JSON file. """
        
        try:
            return dictionary[key]
        except:
            print("Key \"{}\" is not defined in \"{}\"".format(key,dictionary))
            return None
