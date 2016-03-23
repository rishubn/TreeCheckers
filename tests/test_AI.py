import pytest, math, numpy
import backend.AI as AI
from backend.Node import Node
from backend.BoardManager import BoardManager
def testGenerateMoveMap():
    root = Node(50,50,0)
    degree = 90
    expected = {0:[(100,50),(50,100),(0,50),(50,0)]}
    moveMap = AI.generateMoveMap(root,50,degree)
    print(moveMap)
    assert expected == moveMap

def testGenerateMoveMap2Nodes():
    root = Node(50,50,0)
    child = Node(100,100,1)
    root.addChild(child)
    degree = 90
    expected = {0:[(100,50),(50,100),(0,50),(50,0)], 1:[(150,100),(100,150),(50,100),(100,50)]}
    moveMap = AI.generateMoveMap(root,50,degree)
    assert expected == moveMap

def testGeneratePriorityMap():
	depth = 2
	children = 2
	bm = BoardManager(1000,1000, {'startDepth':depth, 'numChildren':children},True)
	bm.buildPlayer();
	priorityMap = AI.generatePriorityMap(bm.players[0]["root"])
	expected = {0: 0.0, 1: 0.3333333333333333, 2: 2.0, 3: 2.0, 4: 0.3333333333333333, 5: 2.0, 6: 2.0}
	assert expected == priorityMap

def testApplyMove():
    depth = 2
    children = 2
    bm = BoardManager(1000,1000, {'startDepth':depth, 'numChildren':children})
    expected = [bm.roots[0].children[1].x, bm.roots[0].children[1].y]
    newBoardState = AI.applyMove(bm.roots, 1, [100,100])
    assert expected != [newBoardState[0].children[1].x, newBoardState[0].children[1].y]
