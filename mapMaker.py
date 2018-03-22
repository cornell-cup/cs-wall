import json


class MapMaker(): 

    #Keys to access JSON data
    BACKGROUND = "BACKGROUND"
    SQUARE_UNIT = "SQUARE_UNIT"

    BOUNDARY = "BOUNDARY"
    BOUNDARY_X = "BOUNDARY_X"
    BOUNDARY_Y = "BOUNDARY_Y"
    
    START = "START"
    START_X = "START_X"
    START_Y = "START_Y"
    
    GOAL = "GOAL"
    GOAL_X = "GOAL_X"
    GOAL_Y = "GOAL_Y"
    
    WALLS = "WALLS"
    WALL_X = "WALL_X"
    WALL_Y = "WALL_Y"

    # Minimap space constants
    FREE_SPACE = 0
    WALL_SPACE = 1

    #game_data constants
    GAME_BACKGROUND = "GAME_BACKGROUND"
    GAME_UNIT = "GAME_UNIT"
    GAME_START = "GAME_START"
    GAME_GOAL = "GAME_GOAL"
    GAME_MAP = "GAME_MAP"


    def __init__(self):
        print "hi"

    def parseMap(self, file_path):
        """Returns a [game_data] from the JSON [file_path]"""

        # json_data = {}
        game_data = {}

        with open("{}.json".format(file_path)) as f:
            json_data = json.load(f)

            #####Interpret JSON

            ### Specify background image

            background = self.accessField(json_data, self.BACKGROUND)

            game_data.update({self.GAME_BACKGROUND: background})

            ### Create map from boundaries
            boundary = self.accessField(json_data,self.BOUNDARY)

            if not boundary:
                return game_data

            # if not boundary:
            #     print("Boundary of map not defined")
            #     break            

            boundary_x = self.accessField(boundary,self.BOUNDARY_X)
            boundary_y = self.accessField(boundary,self.BOUNDARY_Y)

            if ((not boundary_x) or (not boundary_y)):
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


            ### Establish starting location
            start = self.accessField(json_data,self.START)

            if not start:
                return game_data

            start_x = self.accessField(start,self.START_X)
            start_y = self.accessField(start,self.START_Y)

            if ((not start_x) or (not start_y)):
                return game_data

            #Add map to game data
            game_data.update({self.GAME_START:(start_x,start_y)})


            ### Establish goal location
            goal = self.accessField(json_data,self.GOAL)

            if not goal:
                return game_data

            goal_x = self.accessField(goal,self.GOAL_X)
            goal_y = self.accessField(goal,self.GOAL_Y)

            if ((not goal_x) or (not goal_y)):
                return game_data

            #Add map to game data
            game_data.update({self.GAME_GOAL:(goal_x,goal_y)})


            ### Establish unit conversion
            unit = self.accessField(json_data,self.SQUARE_UNIT)

            if not unit:
                return game_data

            #Add map to game data
            game_data.update({self.GAME_UNIT:unit})


        if not f:
            print("File {}.json could not be read".format(file_path))

        return game_data

    def accessField(dictionary,key):

        try:
            return dictionary.get(key)
        except:
            print("Key \"{}\" is not properly defined in \"{}\"".format(key,dictionary))
            return None
