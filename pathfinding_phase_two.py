import math
import sys
import random

# Scenario:
# There is a self-driving vehicle operates on a 10x10 grid
# This program finds the shortest route from start (0,0) to destination 
# (9,9) while avoiding obstacles on (9,7), (8,7), (6,7) and (6,8)

# The A* algorithm was used to solve this problem as the heuristic used to check
# paths which are likely to be shorter first saves time

class Tile:
    """Represents a single tile in the 2 dimensional grid the self driving vehicle is operating on
       This tile may contain an obstacle"""

    def __init__(self, symbol, x, y):

        # Symbol used to represent if an obstacle is on the tile
        self.symbol = symbol

        # Parent used to keep track of previous tile in a path
        self.parent = None
        self.y = y
        self.x = x

        # g represents the shortest currently found distance from the start tile
        self.g = -1

        # h represents the result of the heuristic estimating how far the tile is from the destination
        self.h = -1

    def f(self):
        """f simply returns the sum of how long the current path is (g), and how long is estimated to go(h)"""
        return self.g + self.h

    def diagonal_distance(self, x, y):
        """Returns the number of square the passed coordinates are from the tile while moving like a King in 
           chess, which the self driving car will"""
        x_dist = abs(self.x-x)
        y_dist = abs(self.y-y)

        if (x_dist > y_dist):
            return x_dist
        else:
            return y_dist


def print_grid(grid, GRID_SIZE):
    """Prints the grid showing the empty squares and obstacles"""
    for y in range(GRID_SIZE-1, -1, -1):
        for x in range(GRID_SIZE):
            print('[' + grid[x][y].symbol + ']', end=" ")
        print ('\n', end="")

def find_path(start, destination, grid, GRID_SIZE, OBSTACLE):
    """Sets the parent references of the tiles so if there is a shortest path 
       from the start to the destination, it is represented as a linked list using
       the parent references"""

    PATH = 'O'

    # The open_paths list keeps track of tiles which have a possible path to 
    # the destination, which will initially just be the start tile
    open_paths = [start]
    
    # g is a measurement of distance from start square, so will be 0 for the start square
    start.g = 0

    # while there are possible paths to the destination
    while (len(open_paths) > 0):

        # Get the tile which has the lowest f value out of the
        # tiles with a possible path to the destination
        # This tile is the most likely to have the shortest path to the destination
        current_tile = open_paths[0]
        min_f = current_tile.f()

        for open_path in open_paths:
            if (open_path.f() < min_f):
                min_f = open_path.f()
                current_tile = open_path
    
        # Traverse through neighbours which are adjacent to the current_tile
        for neighbour_x in range(current_tile.x-1, current_tile.x+2):

            # Check coordinates are in valid range
            if (neighbour_x < 0 or neighbour_x >= GRID_SIZE):
                continue

            for neighbour_y in range(current_tile.y-1, current_tile.y+2):

                # Check coordinates are in valid range and the neighbour tile is not an obstacle
                if (neighbour_y < 0 or neighbour_y >= GRID_SIZE or grid[neighbour_x][neighbour_y].symbol == OBSTACLE):
                    continue
            
                neighbour = grid[neighbour_x][neighbour_y]

                # If destination has been reached
                if (neighbour == destination):

                    # Set parent reference of destination to complete shortest path linked list
                    destination.parent = current_tile

                    return                    

                # Calculate heuristic (diagonal distance) of how far away neighbour is from the destination 
                neighbour.h = neighbour.diagonal_distance(9,9)

                # If the neighbour is not already part of a shorter path, represented by smaller distance from start square (g)
                if (neighbour.g == -1 or neighbour.g > current_tile.g + 1):

                    # Calculate distance from neighbour to start square
                    neighbour.g = current_tile.g + 1

                    # Update parent reference to represent path as linked list
                    neighbour.parent = current_tile

                    # Record that is it in an active path
                    if (neighbour not in open_paths):
                        open_paths.append(neighbour)

        # Options beyond this tile have been added to open_paths so current_tile not required in open_paths anymore
        open_paths.remove(current_tile)

def load_obstacles(grid, n, start, destination, GRID_SIZE, OBSTACLE):
    """Randomly place n new obstacles on the grid"""

    # Potential tiles to place obstacles on are the tiles which are 
    # not the start or destination and do not have an obstacle
    options = [grid[x][y] for x in range(GRID_SIZE) for y in range(GRID_SIZE) if grid[x][y] not in [start, destination] and grid[x][y].symbol != OBSTACLE]

    length = len(options)
    
    # If too many obstacles have been requested, place as many obstacles as 
    # possible by setting n so that every potential tile will have an obstacle
    if (length < n):
        n = length

    coordinates = []
    
    # Place n obstacles on the grid by choosing a random option to put an obstacle 
    # on, then removing it as an option and repeating this n times
    for i in range(n):
        chosen_tile = options[random.randrange(length)]
        chosen_tile.symbol = OBSTACLE
        coordinates.append("(" + str(chosen_tile.x) + "," + str(chosen_tile.y) + ")")
        options.remove(chosen_tile)
        length = length-1

    # Print obstacle locations
    print("In addition to the obstacles at (9,7), (8,7), (6,7) and (6,8), more obstacles were placed at:")
    print("[" + ",".join(coordinates) + "]\n") 

def main():
    """Prints the grid, and the optimal path the self driving car will take from start to destination while avoiding the obstacles"""

    EMPTY = ' '
    OBSTACLE = 'X'
    GRID_SIZE = 10

    # Loads the grid with Tile objects
    grid = [[Tile(EMPTY, x, y) for y in range(GRID_SIZE)] for x in range(GRID_SIZE)]
   
    # Create the obstacles
    grid[9][7].symbol = OBSTACLE
    grid[8][7].symbol = OBSTACLE
    grid[6][7].symbol = OBSTACLE
    grid[6][8].symbol = OBSTACLE

    start = grid[0][0]
    destination = grid[9][9]

    # Add 20 more random obstacles
    load_obstacles(grid, 20, start, destination, GRID_SIZE, OBSTACLE)

    # Create linked list using parent references in the tile objects to represent the shortest path from start to destination, if one exists
    find_path(start, destination, grid, GRID_SIZE, OBSTACLE)

    # If the destination's parent reference is None, there is no valid path from the start to the destination
    if (destination.parent == None):
        print("Could not find a path from start to destination.")
    else:
        print("This is a path from the start to the destination\n")
        
        current_tile = destination
        coordinates = []
        
        # Traverse the linked list representing the path and change the symbols to denote the path
        # Also record the coordinates
        while(current_tile != None):
            current_tile.symbol = 'O'
            coordinates.insert(0, "(" + str(current_tile.x) + "," + str(current_tile.y) +")") 
            current_tile = current_tile.parent   
            
        # Print the grid, coordinates and length of path
        print_grid(grid, GRID_SIZE)
        print()
        print("[" + ",".join(coordinates) + "]\n")
        print("This is " + str(len(coordinates) - 1) + " steps")

# Run the main function if this file is being directly run
if __name__=="__main__":
    main()