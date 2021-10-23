# Author: Karthik Reddy Pagilla

import itertools
import math

# global variables
goal = None
initialSide = 1

# State class to store the current state after every action
class State:
    def __init__(self, cannibalsOnLeft, missionariesOnLeft, boatPosition, cannibalsOnRight, missionariesOnRight):
        self.cannibalsOnLeft = cannibalsOnLeft
        self.missionariesOnLeft = missionariesOnLeft
        self.boatPosition = boatPosition
        self.cannibalsOnRight = cannibalsOnRight
        self.missionariesOnRight = missionariesOnRight
        self.Parent = None
    
    def isGoal(self):
        global initialSide

        if (initialSide == 1):
            return ((self.cannibalsOnLeft == 0) and (self.missionariesOnLeft == 0))
        elif (initialSide == 0):
            return ((self.cannibalsOnRight == 0) and (self.missionariesOnRight == 0))

    def isValid(self):
        return (((self.cannibalsOnLeft >= 0) and (self.missionariesOnLeft >= 0))
                and ((self.cannibalsOnRight >= 0) and (self.missionariesOnRight >= 0))
                and ((self.missionariesOnLeft == 0) or (self.missionariesOnLeft >= self.cannibalsOnLeft))
                and ((self.missionariesOnRight == 0) or (self.missionariesOnRight >= self.cannibalsOnRight)))
        
    def __eq__(self, other):
        return ((self.cannibalsOnLeft == other.cannibalsOnLeft) and (self.missionariesOnLeft == other.missionariesOnLeft)
                and (self.boatPosition == other.boatPosition) and (self.missionariesOnRight == other.missionariesOnRight)
                and (self.cannibalsOnRight == other.cannibalsOnRight))

    # hash is requried for comparisions in set     
    def __hash__(self):
        return hash((self.cannibalsOnLeft, self.missionariesOnLeft, self.boatPosition, self.cannibalsOnRight, self.missionariesOnRight))

    def __str__(self):
        return str((self.cannibalsOnLeft, self.missionariesOnLeft, self.boatPosition, self.cannibalsOnRight, self.missionariesOnRight))

# This method gives all possible moves based on the capacity of the boat
def possibleCombinationMoves(capacity):
	moves = []
	for m in range(capacity + 1):
		for c in range(capacity + 1):
			if 0 < m < c:
				continue
			if 1 <= m + c <= capacity:
				moves.append((m, c))
	return moves

# A method to perform DFS until we find our goal state
def DFS(currentState, visited, possibleMoves):
    global goal

    # Base case
    if currentState.isGoal():
        goal = currentState
        return
    
    # Keeping track of paths to avoid loops
    visited.add(currentState)

    # From LEFT -> RIGHT
    if currentState.boatPosition == 1:
        # Trying each possible move
        for i in range(len(possibleMoves)):
            c,m = possibleMoves[i]

            # Operation Validity check
            if (currentState.cannibalsOnLeft - c >= 0 and currentState.missionariesOnLeft - m >= 0):
                
                # Create new state based on the operation
                newState = State(currentState.cannibalsOnLeft - c, currentState.missionariesOnLeft - m, int(not(currentState.boatPosition)),
                                 currentState.cannibalsOnRight + c, currentState.missionariesOnRight + m)
                
                if (newState.isValid() and (newState not in visited)):
                    newState.Parent = currentState
                    
                    DFS(newState, visited, possibleMoves)
    # From RIGHT -> LEFT                
    else:
        # Trying each possible move
        for i in range(len(possibleMoves)):
            c,m = possibleMoves[i]

            # Operation Validity check
            if (currentState.cannibalsOnRight - c >= 0 and currentState.missionariesOnRight - m >= 0):
                
                # Create new state based on the operation
                newState = State(currentState.cannibalsOnLeft + c, currentState.missionariesOnLeft + m, int(not(currentState.boatPosition)),
                                 currentState.cannibalsOnRight - c, currentState.missionariesOnRight - m)
                
                if (newState.isValid() and (newState not in visited)):
                    newState.Parent = currentState
                    
                    DFS(newState, visited, possibleMoves)

# Utility function to apply DFS based on initial state
def solve():
    global goal
    global initialSide

    # Initial state of 3 cannibals, 3 missionaries and boat on left side
    initialState = State(3,3,1,0,0)
    initialSide = 1 # This says initial bank is on left and everyone should move to right
    visited = set()
    possibleMoves = possibleCombinationMoves(2)
    goal = None

    DFS(initialState, visited, possibleMoves)

    if (not(goal)):
        print("No Solution Found.....")
        return

    path = []

    initialState = goal

    while initialState:
        path.append(initialState)
        initialState = initialState.Parent

    path.reverse()
    
    print("Start")
    print()
    for i in range(len(path)):
        cl, ml, b, cr, mr = (path[i].cannibalsOnLeft, path[i].missionariesOnLeft, path[i].boatPosition, path[i].cannibalsOnRight, path[i].missionariesOnRight)

        if cl == 0:
            print("0", end=" ")
        else:
            print("C"*cl, end=" ")
        if ml == 0:
            print("0", end=" ")
        else:
            print("M"*ml, end=" ")
        if(b == 1):
            print("-->", end=" ")
        elif (b == 0):
            print("<--", end=" ")
        if cr == 0:
            print("0", end=" ")
        else:
            print("C"*cr, end=" ")
        if mr == 0:
            print("0")
        else:
            print("M"*mr)
    print()
    print("Goal Reached")

solve()