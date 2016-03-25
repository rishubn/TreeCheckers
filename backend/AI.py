from backend.Node import Node
import math
import sys
import copy
# @RN March 15 2016
# Sets priority for each node based on depth / children of node
# Nodes without children that are lower in the tree are prioritized higher than higher nodes with children
def generatePriorityMap(root,depth=0,priorityMap={}):
    if root:
        priorityMap[root.ID] = (depth / (len(root.children) + 1))
        for ids, child in root.children.items():
            generatePriorityMap(child,depth+1)
    return priorityMap

# @RN March 15 2016
# Generates possible moves for a root node and all its children
# Returns map with node.ID as key and a list of tuples of possible moves
# segmented by an angle
# Ex: {1: [
#   (radius*cos(theta),radius*sin(theta)),
#   (radius*cos(2*theta),radius*sin(2*theta)),
#    ....
#   (radius*cos(n*theta),radius*sin(n*theta))]}
# n = 2pi / theta
def generateMoveMap(root, radius, degree=10,radian=False,segments=0,moveMap={}):
    if not radian:
        degree = math.radians(degree)
        radian = True
    if segments == 0:
        segments = int(round(2*math.pi / degree,0))
    if root:
        moveMap[root.ID] = []
        for i in range(segments):
            moveMap[root.ID].append((round(root.x + radius*math.cos(i*degree),0),round(root.y +
                radius*math.sin(i*degree),0)))
        for ids, child in root.children.items():
            print(child.ID)
            generateMoveMap(child,radius,degree,radian,segments,moveMap)
    return moveMap

#@FCC March 2016
#TODO: generalize this to any number of players
#board is a list of nodes, depth is an integer, degree is a number, moveradius is a number, and pnum is an integer
#returns the value of a move
#these nodes are NOT game nodes, they are gamestates. Their children are subsequent game states.
def minimax(board, depth, degree, moveradius, pnum):
    if depth == 0 or len(node.children) == 0:
        return heuristic(board)

    if pnum == 0: #max
        moveMap = {}
        for root in board:
            moveMap.update(generateMoveMap(root = root, radius = moveradius))
        
        bestvalue = sys.float_info.max
        for nodeId in movemap:
            for move in movemap[nodeId]:
                value = minimax(applyMove(board, nodeId, move), depth - 1, 1)
                bestvalue = max(value, bestvalue)
    else: #min
        moveMap = {}
        for root in board:
            movemap.update(generateMoveMap(root = root, radius = moveradius))
        
        bestvalue = sys.float_info.min
        for nodeId in moveMap:
            for move in movemap[nodeId]:
                value = minimax(applyMove(board, nodeId, move), depth - 1, 0)
                bestvalue = min(bestvalue, value)
    return value

#bs is a board state (a list of roots)
def heuristic(bs):
    return 0

# @RN March 22 2016
# takes the board state and a node ID and a new location and applies it to the node
# returns a new board state
def applyMove(bs, nodeId, location):
    newBs = copy.deepcopy(bs)
    for root in newBs:
        node = root.getNode(nodeId)
        if node is not None:
            node.x = location[0]
            node.y = location[1]
    return newBs

#@FCC March 2016
#thebs is the current board state, represented as a list of root nodes
def getOptimalMove(thebs, depth, degree, moveradius, pnum):
    bestMove = None
    bestMoveValue = sys.float_info.min
    for move in moveMap: #might be wrong
        value = minimax(thebs, depth, degree, moveradius, pnum)
        if value >= bestMoveValue:
            bestMoveValue = value
            bestMove = move
    return bestMove
