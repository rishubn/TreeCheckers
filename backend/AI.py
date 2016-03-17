from backend.Node import Node
import math
import sys
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
# Generates possible moves for a root node and all it's children
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




#returns the value of a move
#these nodes are NOT game nodes, they are gamestates. 
def minimax(board, depth, pnum):
    if depth == 0 or len(node.children) == 0:
        return heuristic(board)

    if pnum == 0: #max
        bestvalue = sys.float_info.max
        for move in moveMap: #probably wrong
            value = minimax(move, depth - 1, 1)
            bestvalue = max(value, bestvalue)
    else: #min
        bestvalue = sys.float_info.min
        for move in moveMap: #ditto
            value = minimax(move, depth - 1, 0)
            bestvalue = min(bestvalue, value)
    return value

#bs is a board state (a list of roots)
def heuristic(bs):
    return 0

#thebs is the current boar state
def getMove(thebs, depth, pnum):
    bestMove = None
    bestMoveValue = sys.float_info.min
    for move in moveMap: #might be wrong
        value = minimax(thebs, depth, pnum)
        if value >= bestMoveValue:
            bestMoveValue = value
            bestMove = move
    return bestMove
