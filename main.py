#!/usr/bin/env python
"""
Cave generator, based on the following article:
http://gamedevelopment.tutsplus.com/tutorials/generate-random-cave-levels-using-cellular-automata--gamedev-9664
"""

from random import random

width = 100
height = 100
chanceToStartAlive = 0.45
birthLimit = 4
deathLimit = 4
numberOfSteps = 7


def initialiseMap(grid):
    for x in range(0, width):
        for y in range(0, height):
            if random() < chanceToStartAlive:
                grid[y][x] = True
    return grid


# Returns the number of cells in a ring around (x,y) that are alive.
def countAliveNeighbours(grid, x, y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            neighbour_x = x + i
            neighbour_y = y + j
            # If we're looking at the middle point
            if i == 0 and j == 0:
                # Do nothing, we don't want to add ourselves in!
                pass
            elif (neighbour_x < 0 or
                    neighbour_y < 0 or
                    neighbour_x >= len(grid) or
                    neighbour_y >= len(grid[0])):
                # In case the index we're looking at it off the edge of the map
                count += 1
            elif grid[neighbour_x][neighbour_y]:
                # Otherwise, a normal check of the neighbour
                count = count + 1
    return count


def doSimulationStep(oldMap):
    newMap = [[False for x in range(width)] for y in range(height)]
    # Loop over each row and column of the map
    for x in range(0, len(oldMap)):
        for y in range(0, len(oldMap[0])):
            nbs = countAliveNeighbours(oldMap, x, y)
            # The new value is based on our simulation rules
            # First, if a cell is alive but has too few neighbours, kill it.
            if oldMap[x][y]:
                if nbs < deathLimit:
                    newMap[x][y] = False
                else:
                    newMap[x][y] = True
            else:
                # Otherwise, if the cell is dead now, check if it has the right
                # number of neighbours to be 'born'
                if nbs > birthLimit:
                    newMap[x][y] = True
                else:
                    newMap[x][y] = False
    return newMap


def generateMap():
    # Create a new map
    cellmap = [[False for _ in range(width)] for _ in range(height)]
    # Set up the map with random values
    cellmap = initialiseMap(cellmap)
    # And now run the simulation for a set number of steps
    for _ in range(0, numberOfSteps):
        cellmap = doSimulationStep(cellmap)
    return cellmap


def display(grid):
    line = "\n"
    color = {
            "cave": '\033[44m',
            "wall": '\033[100m'
    }
    ENDC = '\033[0m'
    for x in range(0, width):
        for y in range(0, height):
            if grid[y][x]:
                line += "{} {}".format(color["wall"], ENDC)
            else:
                line += "{} {}".format(color["cave"], ENDC)

        line += "\n"
    return line


print(display(
    generateMap()
))
