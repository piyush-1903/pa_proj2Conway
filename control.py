import numpy as np # we'll use numpy arrays as the basis for our grids. 

# Set up a random number generator from numpy.
RNG = np.random.default_rng()

# Parameters that can be changed in this file: number of states, grid dimensions, 
# neighbors function, rules function, grid initialization function.
# These parameters are set as global variables at the end of this file.

# If you want to change visualization parameters (cell size in window, padding, 
# gif filename, ...) see display.py

class Grid:
    # Note that the first index in a 2D array refers to the row (vertical) coordinate
    # while the second index refers to the column (horizontal) coordinate
    # That order is opposite our normal (x,y) coordinate system, so we need to remember
    # to use (y,x) when indexing into the data.
    gridSize: tuple[int, int] # rows, columns == y,x
    data: np.ndarray 
    generations: int 

    def __init__(self, size, setup):
        # YOUR CODE HERE
        self.gridSize = size
        self.data = setup(size)
        self.generations = 0
        # Remember to set object attributes self.gridSize and self.data.
        self.generations = 0

#--------------------------------------------------------------------
# Initialization functions -- used by the constructor. Only one is used
# in any game definition. You may add your own for the creative exercise.
#--------------------------------------------------------------------

# function: randStart
# Purpose: employed by grid __init__ (constructor) to give initial value to data
# param: size
# returns: an np array of size size, whose values are uniformly selected from range(states)
def randStart(size):
    # YOUR CODE HERE
    # To get your random numbers, you must use the generator from numpy.random which 
    # is stored in the global variable RNG defined above.
    # See https://numpy.org/doc/stable/reference/random/index.html#random-quick-start    
    return RNG.integers(low=0, high=NUM_STATES, size=size)

# function: glideStart
# Purpose: employed by grid __init__ (constructor) to give initial value to data
# param: size
# returns: an np array of size size, whose values are all zero, except for positions
# (2,0), (0,1), (2,1), (1,2), and (2,2), whose values are 1. Intended to be used
# on a game w 2 states.
def glideStart(size):
    # YOUR CODE HERE
    grid = np.zeros(size, dtype=int)
    coords = [(0,2), (1,0), (1,2), (2,1), (2,2)]
    for y, x in coords:
        if y < size[0] and x < size[1]:
            grid[y][x] = 1
    return grid

# --------------------------------------------------------------------
# Rule functions -- used by the evolve function. Only one is used
# in any game definition. You MUST add a new one for the creative exercise.
# --------------------------------------------------------------------

# function: ruleGOL
# purpose: applies a set of rules given a current state and a set of tallies over neighbor states
# params: cell, an element from range(states), where states is the global variable
#           tallies, tallies[k] = number of neighbors of state k, for all k in the range of states
# returns: a new state based on the classic rules of the game of life.
#           See https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
# Note: assumes a two-state game, where 0 is "dead" and 1 is "alive"
def ruleGOL(cell, tallies):
    # YOUR CODE HERE
    alive_neighbors = tallies[1]
    if cell == 1:
        return 1 if alive_neighbors in [2, 3] else 0
    else:
        return 1 if alive_neighbors == 3 else 0


# function: ruleCycle
# purpose: applies a set of rules given a current state and a set of tallies over neighbor states
# params: cell, an element from range(states), where states is the global variable
#           tallies, tallies[k] = number of neighbors of state k, for all k in the range of states
# returns: if k is the current state, returns k+1 if there is a neighbor of state k+1, else returns k
#          See https://en.wikipedia.org/wiki/Cyclic_cellular_automaton
def ruleCycle(cell, tallies):
    next_state = (cell + 1) % NUM_STATES
    return next_state if tallies[next_state] > 0 else cell


# --------------------------------------------------------------------
# Neighbor functions -- used by the evolve function. Only one is used
# in any game definition. You may add your own for the creative exercise.
# --------------------------------------------------------------------
# returns a list of neighbors in a square around x,y
def neighborSquare(x, y):
    return [(x+dx, y+dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if not (dx == 0 and dy == 0)]


# returns a list of neighbors in a diamond around x,y (NWSE positions)
def neighborDiamond(x, y):
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]


# function: tally_neighbors
# purpose: counts a given cell's the neighbors' states
# params: grid, an np array of data from a grid, containing states of all cells
#         position, the current cell position (a Tuple)
#         neighborSet, a function that when called on position x,y returns a list of x,y's neighbors
# returns: a list whose entries, tally[k] are the number of valid neighbors of x,y whose state is k.
# Note: neighborSet may not necessarily return *valid* neighbors. It's tally_neighbor's job to check
# for validity.
def tally_neighbors(grid, position, neighborSet):
    max_state = NUM_STATES
    tally = [0] * max_state
    y, x = position  # FIXED: interpret position as (row, column)
    for dx, dy in neighborSet(x, y):
        if 0 <= dy < grid.shape[0] and 0 <= dx < grid.shape[1]:
            tally[grid[dy][dx]] += 1
    return tally


# student: putting it all together.
# function: evolve
# purpose: to increment the automata by *one* time step. Given an array representing the automaton at the
# start of the time step (the start grid), this function creates an array for the end of the time step
# (the end grid) by applying the rule specified in function apply_rule to every position in the array.
# Note that all rule evaluation is done on the start grid, but the new state is set in the end grid.
# This function *changes* the input parameter to the new state. 
# The grid's generations variable should be incremented every time the function is called. (This variable
# may only be useful for debugging--there is a lot we *could* do with it, but our application doesn't use it.)
def evolve(g, apply_rule, neighbors) -> None:
    new_data = np.copy(g.data)
    for x in range(g.gridSize[0]):
        for y in range(g.gridSize[1]):
            position = (x, y)
            tallies = tally_neighbors(g.data, position, neighbors)
            new_data[x][y] = apply_rule(g.data[x][y], tallies)
    g.data = new_data
    g.generations += 1


# Here we define some global (to the module) variables which will determine what CA to run.
# You will want to change these values to test out other choices for the CA elements / parameters.
NUM_STATES = 2
WHICH_GRID = Grid((50,50), randStart)
WHICH_RULE = ruleGOL
WHICH_NEIGHBOR = neighborSquare

# Should we save a gif of the animation?
# (Set the parameters (including filename) of the animation in display.py)
SAVE_ANIMATION = True

