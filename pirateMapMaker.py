import json
import Globals as g


class PirateMapMaker():
    """Object class for making levels for Wall from JSON files

       Contains the keywords for parsing a level JSON into
       a data structure representing the game state for the GUI.
    """

    ###Keys to access JSON data

    #Background image for game
    BACKGROUND = "BACKGROUND"

    #Starting direction of the robot
    DIRECTION = "DIRECTION"

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
    ENEMIES = "ENEMIES"
    ENEMY_DIRECTION = "ENEMY_DIRECTION"
    ENEMY_PATH = "ENEMY_PATH"
    # ENEMY_X = "ENEMY_X"
    # ENEMY_Y = "ENEMY_Y"

    #Cardinal directions
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"


    ###Constants to create game_data

    #Keys to parse game_data dictionary

    #References a string
    GAME_BACKGROUND = "GAME_BACKGROUND"
    # References a direction global
    GAME_START_DIRECTION = "GAME_START_DIRECTION"
    # References a tuple in the format (x,y)
    GAME_START = "GAME_START"
    # References a tuple in the format (x,y)
    GAME_GOAL = "GAME_GOAL"
    # References a 2D list (minimap) where rows represent y values and columns are x values
    GAME_MAP = "GAME_MAP"
    # References a list of dictionaries
    GAME_ENEMIES = "GAME_ENEMIES"
    # Within GAME_ENEMIES, references a direction global
    GAME_ENEMY_DIRECTION = "ENEMY_DIRECTION"
    # # Within GAME_ENEMIES, references a list of tuples in the format (x,y)
    GAME_ENEMY_PATH = "ENEMY_PATH"

    # Minimap space constants
    FREE_SPACE = 0
    OBSTACLE_SPACE = 1

    def __init__(self,name=None):
        #TODO: Decide if we need this field for GUI processing
        self.name = name

    def parseMap(self, file_path):
        """Returns a dictionary [game_data] representing the game state
        from the JSON given in [file_path]

        :param file_path string representing the filepath to the JSON file
        :return dictionary with the game state

        """

        game_data = {}

        if not file_path[-5:0]==".json":
            file_path = "{}.json".format(file_path)

        with open(file_path,"r") as f:
            json_data = json.load(f)

            #TODO: Determine location of level files and decide if name parsing is necessary 
            #(i.e. "level_5" compared to "levels/level_5")
            self.name = file_path

            #####Interpret JSON

            ### Specify background image

            background = self.accessField(json_data, self.BACKGROUND)

            game_data.update({self.GAME_BACKGROUND: background})

            ### Create map from boundaries
            boundary = self.accessField(json_data,self.BOUNDARY)

            if not boundary:
                print("Please define a value for {}".format(self.BOUNDARY))
                return game_data

            boundary_x = self.accessField(boundary,self.BOUNDARY_X)
            boundary_y = self.accessField(boundary,self.BOUNDARY_Y)

            if boundary_x==None:
                print("Please define a valid number for {}".format(self.BOUNDARY_X))
                return game_data

            if boundary_y==None:
                print("Please define a valid number for {}".format(self.BOUNDARY_Y))
                return game_data

            map_data = []

            for unit in range(boundary_y):
                map_data.append([self.FREE_SPACE]*boundary_x)

            # Add map to game data
            game_data.update({self.GAME_MAP: map_data})

            ### Add enemies to map
            enemies = self.accessField(json_data, self.ENEMIES)

            enemy_data = []

            for enemy in enemies:
                enemy_direction = self.accessField(enemy, self.ENEMY_DIRECTION)
                enemy_path = self.accessField(enemy, self.ENEMY_PATH)

                enemy = {}
                direction = ""
                path = []

                if enemy_direction == self.NORTH:
                    direction = g.NORTH
                elif enemy_direction == self.EAST:
                    direction = g.EAST
                elif enemy_direction == self.SOUTH:
                    direction = g.SOUTH
                elif enemy_direction == self.WEST:
                    direction = g.WEST
                else:
                    print("Please define a valid value for {} ('{}', '{}', '{}', '{}')".format(
                        self.ENEMY_DIRECTION, self.NORTH, self.EAST, self.SOUTH, self.WEST))
                    return game_data

                for point in enemy_path:
                    space = (point[0],point[1])
                    path.append(space)

                enemy.update({self.GAME_ENEMY_DIRECTION:direction, self.GAME_ENEMY_PATH:path})
                enemy_data.append(enemy)

            #Add enemies to game data
            game_data.update({self.GAME_ENEMIES:enemy_data})

            ### Establish starting location
            start = self.accessField(json_data,self.START)

            if not start:
                print("Please define a value for {}".format(self.START))
                return game_data

            start_x = self.accessField(start,self.START_X)
            start_y = self.accessField(start,self.START_Y)

            if start_x==None:
                print("Please define a valid number for {}".format(self.START_X))
                return game_data

            if start_y==None:
                print("Please define a valid number for {}".format(self.START_Y))
                return game_data

            #Add map to game data
            game_data.update({self.GAME_START:(start_x,start_y)})


            ### Establish goal location
            goal = self.accessField(json_data,self.GOAL)

            if not goal:
                print("Please define a value for {}".format(self.GOAL))
                return game_data

            goal_x = self.accessField(goal,self.GOAL_X)
            goal_y = self.accessField(goal,self.GOAL_Y)

            if goal_x==None:
                print("Please define a valid number for {}".format(self.GOAL_X))
                return game_data

            if goal_y==None:
                print("Please define a valid number for {}".format(self.GOAL_Y))
                return game_data

            #Add map to game data
            game_data.update({self.GAME_GOAL:(goal_x,goal_y)})


            ### Establish unit conversion
            direction = self.accessField(json_data,self.DIRECTION)

            if direction == self.NORTH:
                # game_direction = g.NORTH
                game_data.update({self.GAME_START_DIRECTION: g.NORTH})
            elif direction == self.EAST:
                # game_direction = g.EAST
                game_data.update({self.GAME_START_DIRECTION: g.EAST})
            elif direction == self.SOUTH:
                # game_direction = g.SOUTH
                game_data.update({self.GAME_START_DIRECTION: g.SOUTH})
            elif direction == self.WEST:
                # game_direction = g.WEST
                game_data.update({self.GAME_START_DIRECTION: g.WEST})
            else:
                print("Please define a valid value for {} ('{}', '{}', '{}', '{}')".format(
                    self.DIRECTION, self.NORTH, self.EAST, self.SOUTH, self.WEST))
                return game_data

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
