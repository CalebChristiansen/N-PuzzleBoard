import random
import copy
import math

from basicsearch_lib.board import Board

class TileBoard(Board):
    def __init__(self, n, multiple_solutions=False, force_state=None,
                 verbose=False):
        """"TileBoard(n, multiple_solutions
        Create a tile board for an n puzzle.
        
        If multipleSolutions are true, the solution need not
        have the space in the center.  This defaults to False but
        is automatically set to True when there is no middle square 
        
        force_state can be used to initialize an n puzzle to a desired
        configuration.  No error checking is done.  It is specified as
        a list with n+1 elements in it, 1:n and None in the desired order.

        verbose is a boolean for turning on debugging
        """
        
        self.verbose = verbose  # not debug state, up to you to use it
        
        self.boardsize = int(math.sqrt(n+1))
        if math.sqrt(n+1) != self.boardsize:
            raise ValueError("Bad board size\n" +
                "Must be one less than an odd perfect square 8, 24, ...")

        # initialize parent
        super().__init__(self.boardsize, self.boardsize)

        if (self.verbose):
            print("Debug Mode")

        # Compute solution states
        # todo:  Set self.goals to a list of solution tuples
        # If multiple_solutions is true, None can be anywhere:
        # [(None,1,2,3,...), (1,None,2,3,...), (1,2,None,3,...)]
        # Otherwise, must be the last square:  [(1,2,3,...,None)]

        # Create a list of solutions first. It's easier. Then convert to tuple.
        goalState = [] #a state of a solvable board
        self.goals = []     #the list of all solvable boards
        if (multiple_solutions):
            for y in range(n+1): #boardsize is 1 larger than n
                for x in range(n):
                    if (self.verbose): print("x",x,"y",y)
                    if (y == x):
                        goalState.append(None)
                    goalState.append(x + 1)
                    if (y==n and x==n-1): #special case where the last None needs to be placed
                        goalState.append(None)
                self.goals.append(tuple(goalState))
                goalState.clear()
        else:
            #only one solution with none on the end
            for x in range(n):
                goalState.append(x + 1)
            goalState.append(None)
            self.goals.append(tuple(goalState))

        if (verbose): print(self.goals)


        # todo:  Determine inital state and make sure that it is solvable
        self.initalBoard = []

        # check for force_state and if it's solvable
        if (force_state != None):
            if (not self.solvable(force_state)):
                raise ValueError("Check force_state solvability")
        # Generate random board
        else:
            while(True): # a do-while loop in python
                self.initalBoard.clear()
                for x in range(n):
                    self.initalBoard.append(x + 1)
                random.shuffle(self.initalBoard)
                self.initalBoard.append(None)
                if (verbose): print(self.initalBoard)

                if (self.solvable(self.initalBoard)): break #end while loop


        # todo:  Populate the board using self.place
        #        It would be wise to track the empty square location as well
        #        as it will make action generation easier

        self.gameBoard = Board(self.boardsize,self.boardsize)
        self.emptySquare = (None,None) #Row and Column location of empty square

        if (verbose): print(self.gameBoard)
        counter = 0
        #make the board using board class
        for x in range(self.boardsize):     # x will be rows
            for y in range(self.boardsize): # y will be columns
                self.gameBoard.place(x,y,self.initalBoard[counter])
                if (self.initalBoard[counter] == None):
                    self.emptySquare = (x,y)
                    print("emptySquare:",self.emptySquare)
                counter += 1

        if(verbose): print(self.gameBoard)



    def solvable(self, tiles, verbose=False):
        """solvable - Determines if a puzzle is solvable

            Given a list of tiles, determine if the N-puzzle is solvable.
            You do not need to know how to do this, but the calculation
            is based on the inversion order.

            for each number in the list of tiles,
               How many following numbers are less than that one
               e.g. [13, 10, 11, 6, 5, 7, 4, 8, 1, 12, 14, 9, 3, 15, 2, None]
               Example:  Files following 9:  [3, 15, 2, None]
               Two of these are smaller than 9, so the inversion order
                   for 9 is 2

            A puzzle's inversion order is the sum of the tile inversion
            orders.  For puzzles with even numbers of rows and columns,
            the row number on which the blank resides must be added.
            Note that we need not worry about 1 as there are
            no tiles smaller than one.

            See Wolfram Mathworld for further explanation:
                http://mathworld.wolfram.com/15Puzzle.html
            and http://www.cut-the-knot.org/pythagoras/fifteen.shtml

            This lets us know if a problem can be solved.  The inversion
            order modulo 2 is invariant across moves.  This means that
            when we make a legal move, the inversion order will always
            be even or odd.  The solution state always has an even
            inversion order, so any puzzle with an odd inversion
            number cannot be solved.
        """

        inversionorder = 0
        # Make life easy, remove None
        reduced = [t for t in tiles if t is not None]
        # Loop over all but last (no tile after it)
        for idx in range(len(reduced)-1):
            value = reduced[idx]
            after = reduced[idx+1:]  # Remaining tiles
            smaller = [x for x in after if x < value]
            numtiles = len(smaller)
            inversionorder = inversionorder + numtiles
            if verbose:
                print("idx {} value {} tail {} #smaller {} sum: {}".format(
                    idx, value, after, numtiles, inversionorder))

        # Even number of rows must take the blank position into account
        if self.get_rows() % 2 == 0:
            if verbose:
                print("Even # rows, adding for position of blank")
            inversionorder = inversionorder + \
                math.floor(tiles.index(None) / self.boardsize)+1

        solvable = inversionorder % 2 == 0  # Solvable if even
        return solvable
                                
    def __hash__(self):
        "__hash__ - Hash the board state"
        
        # Convert state to a tuple and hash
        return hash(self.state_tuple())
    
    def __eq__(self, other):
        "__eq__ - Check if objects equal:  a == b"

        # todo:  Determine if two board configurations are equivalent
        #raise NotImplementedError("Check ==")

        if self.verbose:
            print("other:\n",other)

        #Check sizes match
        if (other.get_rows() != self.gameBoard.get_rows()):
            if self.verbose: print("rows not equal")
            return False
        if (other.get_cols() != self.gameBoard.get_cols()):
            if self.verbose: print("cols not equal")
            return False

        #Check for element equality
        for x in range(self.boardsize):     # x will be rows
            for y in range(self.boardsize): # y will be columns
                if self.gameBoard.get(x,y) != (other.get(x,y)):
                    if self.verbose: print(self.gameBoard.get(x,y)," != ",(other.get(x,y)))
                    return False

        return True



    def state_tuple(self):
        "state_tuple - Return board state as a single tuple"

        raise NotImplementedError(
            "You must create a tuple based on the board state")

    def get_actions(self):
        "Return row column offsets of where the empty tile can be moved"

        raise NotImplementedError("Return list of valid actions")

            
    def move(self, offset):
        "move - Move the empty space by [delta_row, delta_col] and return new board"

        # Hint:  Be sure to use deepcopy
        raise NotImplementedError("Return new TileBoard with action applied")

    
    def solved(self):
        "solved - Is the puzzle solved?  Returns boolean"

        raise NotImplementedError("Puzzle in solved state?")
