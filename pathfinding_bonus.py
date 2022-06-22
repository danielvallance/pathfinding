import math
import sys
import random

# Scenario:
# There is a self-driving vehicle operates on a 10x10 grid
# This program finds attempts to find a route from start (0,0) to destination 
# (9,9) while avoiding obstacles on (9,7), (8,7), (6,7) and (6,8) and 20 random additional obstacles

# If no path with no obstacles is found, one with minimal obstacles will be found and the 
# obstacles traversed will be printed

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
        self.h = self.diagonal_distance(9,9)

        # o represents the number of obstacles traversed in the current path - ideally this should be 0
        self.o = 0

    def diagonal_distance(self, x, y):
        """Returns the number of square the passed coordinates are from the tile while moving like a King in 
           chess, which the self driving car will"""
        x_dist = abs(self.x-x)
        y_dist = abs(self.y-y)

        if (x_dist > y_dist):
            return x_dist
        else:
            return y_dist

    def f(self):
        """f simply returns the sum of how long the current path is (g), and how long is estimated to go(h)"""
        return self.g + self.h


def print_grid(grid, GRID_SIZE):
    """Prints the grid showing the empty squares and obstacles"""
    for y in range(GRID_SIZE-1, -1, -1):
        for x in range(GRID_SIZE):
            print('[' + grid[x][y].symbol + ']', end=" ")
        print ('\n', end="")

def find_path(start, destination, grid, GRID_SIZE, OBSTACLE, PATH):
    """Sets the parent references of the tiles so if there is a shortest path 
       from the start to the destination, it is represented as a linked list using
       the parent references"""

    # The open_paths list keeps track of tiles which have a possible path to 
    # the destination, which will initially just be the start tile
    open_paths = [start]
    
    # g is a measurement of distance from start square, so will be 0 for the start square
    start.g = 0

    # while there are possible paths to the destination
    while (len(open_paths) > 0):
        
        # Get the tile which has the lowest number of obstacles traversed and 
        # then the lowest f value out of the currently open paths
        # This path will have traversed the least obstacles and is the most 
        # likely to have the shortest path to the destination
        current_tile = open_paths[0]
        min_f = current_tile.f()
        min_obs = current_tile.o

        for open_path in open_paths:
            if (open_path.o < min_obs or open_path.o == min_obs and open_path.f() < min_f):
                min_f = open_path.f()
                min_obs = open_path.o
                current_tile = open_path
    
        # Traverse through neighbours which are adjacent to the current_tile
        for neighbour_x in range(current_tile.x-1, current_tile.x+2):

            # Check coordinates are in valid range
            if (neighbour_x < 0 or neighbour_x >= GRID_SIZE):
                continue

            for neighbour_y in range(current_tile.y-1, current_tile.y+2):

                # Check coordinates are in valid range
                if (neighbour_y < 0 or neighbour_y >= GRID_SIZE):
                    continue
            
                neighbour = grid[neighbour_x][neighbour_y]

                # If destination has been reached
                if (neighbour == destination):

                    # Set parent reference of destination to complete shortest path linked list
                    destination.parent = current_tile

                    # Record obstacles crossed
                    destination.o = current_tile.o

                    return                    

                # If the neighbour is not already part of a shorter path or one with less obstacles
                if (neighbour.g == -1 or neighbour.o > current_tile.o + 1 or neighbour.o == current_tile.o + 1 and neighbour.g > current_tile.g + 1):

                    # Calculate distance from neighbour to start square
                    neighbour.g = current_tile.g + 1

                    # Calculate obstacles encountered on path
                    if (neighbour.symbol == OBSTACLE):
                        neighbour.o = current_tile.o + 1
                    else:
                        neighbour.o = current_tile.o

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
    TRAVERSED = '+'
    PATH = 'O'
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
    find_path(start, destination, grid, GRID_SIZE, OBSTACLE, PATH)

    if (destination.o > 0):
        print("Unable to reach delivery point\n")

    print("This is a path from the start to the destination traversing " + str(destination.o) + " obstacle(s)\n")
        
    current_tile = destination
    coordinates = []
    obstacles = []
        
    # Traverse the linked list representing the path and change the symbols to denote the path
    # Also record the coordinates and obstacles
    while(current_tile != None):
        if (current_tile.symbol == OBSTACLE):
            obstacles.insert(0, "(" + str(current_tile.x) + "," + str(current_tile.y) + ")")
            current_tile.symbol = TRAVERSED
        else:
            current_tile.symbol = PATH

        coordinates.insert(0, "(" + str(current_tile.x) + "," + str(current_tile.y) +")") 
        current_tile = current_tile.parent   
            
    # Print the grid, coordinates and length of path
    print_grid(grid, GRID_SIZE)
    print()
    print("[" + ",".join(coordinates) + "]\n")
    print("This is " + str(len(coordinates) - 1) + " steps\n")
    print("Obstacles were traversed at:\n")
    print("[" + ",".join(obstacles) + "]")

# Run the main function if this file is being directly run
if __name__=="__main__":
    main()