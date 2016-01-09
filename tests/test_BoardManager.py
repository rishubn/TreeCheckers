import pytest, math
from backend.Node import Node
from backend.BoardManager import BoardManager

#this is a helper function for comparing two floating point numbers. 
#probably already exists somewhere but it's so simple we just rewrote it here
def tolerantEquals(a, b, tol):
	return abs(a - b) <= tol

#test the getDistance Function
def testGetDistanceStraightlineEuclidean():
	bm = BoardManager(1000, 1000, {'startDepth':2, 'distanceMetric':'euclidean'})
	assert tolerantEquals(bm.getDistance(0, 0, 0, 1), 1, 0.001)
def testGetDistanceDiagonalEuclidean():
	bm = BoardManager(1000, 1000, {'startDepth':2, 'distanceMetric':'euclidean'})
	assert tolerantEquals(bm.getDistance(0, 0, 1, 1), math.sqrt(2), 0.001)

#test the getNodeDistance convenience function
def testGetNodeDistanceEuclidean():
	bm = BoardManager(1000, 1000, {'startDepth':2, 'distanceMetric':'euclidean'})
	n0 = Node(0, 0, 0)
	n1 = Node(1, 1, 1)
	assert tolerantEquals(bm.getNodeDistance(n0, n1), math.sqrt(2), 0.001)

#test the makeMove function
def testMakeMoveValid():
	bm = BoardManager(1000, 1000, {'startDepth':2})
	assert bm.makeMove(1, 0, 1 + bm.p1Node.x, 1 + bm.p1Node.y) #should return true because it was a valid move
def testMakeMoveInvalidInBounds():
	bm = BoardManager(1000, 1000, {'startDepth':2})
	assert not bm.makeMove(1, bm.p1Node.ID, 25 + bm.p1Node.x, 25 + bm.p1Node.y) #should return false because it was an invalid move because it was too far
def testmakeMoveInvalidOutOfBounds():
	bm = BoardManager(1000, 1000, {'startDepth':2})
	bm.p1Node.x = 1
	assert not bm.makeMove(1, 0, -2 + bm.p1Node.x, bm.p1Node.y) #should return false because it was an invalid move becuase it went outside the playing area

#test the _applyMove function
def test_ApplyMove():
	bm = BoardManager(1000, 1000, {'startDepth':1})
	bm._applyMove(bm.p1Node, -1, -2) #wouldn't be allowed if there was error checking
	assert bm.p1Node.x == -1 and bm.p1Node.y == -2

#test the isValidMove function
def testIsValidMoveValid():
	bm = BoardManager(1000, 1000, {'startDepth':1})
	assert bm.isValidMove(2, bm.p2Node.ID, bm.p2Node.x + 1, bm.p2Node.y + 1)
def testIsValidMoveInvalidTooFar():
	bm = BoardManager(1000, 1000, {'startDepth':1})
	assert not bm.isValidMove(2, bm.p2Node.ID, bm.p2Node.x + 10000, bm.p2Node.y + 10000)
def testIsValidMoveInvalidOutOfBounds():
	bm = BoardManager(1000, 1000, {'startDepth':1})
	assert not bm.isValidMove(1, bm.p1Node.ID, -100, bm.p1Node.y)


#test the buildTree function
#could really use some more tests, especially of correct placement of children, both in the tree and on the board
def testBuildTreeDepth1p1Node():
	bm = BoardManager(1000, 1000, {'startDepth':1, 'numChildren':1})
	assert bm.p1Node.ID is not None and bm.p1Node.x is not None and bm.p1Node.y is not None and len(bm.p1Node.children) == 1
def testBuildTreeDepth1p2Node():
	bm = BoardManager(1000, 1000, {'startDepth':1, 'numChildren':5})
	assert bm.p2Node.ID is not None and bm.p2Node.x is not None and bm.p2Node.y is not None and len(bm.p2Node.children) == 5
def testBuildTreeDepth2Children():
	bm = BoardManager(1000, 1000, {'startDepth':2, 'numChildren':2})
	assert len((bm.p1Node.children[
            list(bm.p1Node.children.keys())[0]
            ]).children) == 2 and len((bm.p2Node.children[
            list(bm.p2Node.children.keys())[0]]).children) == 2

def testSetIndexesValidIndex():
    depth = 3
    children = 3
    bm = BoardManager(1000,1000, {'startDepth':depth, 'numChildren':children})
    tree = bm.buildTree(depth,children,bm.getNextId())
    bm.setIndexes(tree,children)
    for ids, positions in bm.positionMap.items():
        assert positions[1] != -1 

def testSetIndexesCorrectIndexAndDepth():
	depth = 2
	children = 3
	bm = BoardManager(1000,1000, {'startDepth':depth, 'numChildren':children},True)
	tree = bm.buildTree(depth,children,bm.getNextId())
	bm.setIndexes(tree,children)
	pm = bm.positionMap
	assert pm == {0: [0, 1], 1: [1, 1], 2: [2, 1], 3: [2, 2], 4: [2, 3], 5: [1, 2], 6: [2, 5], 7: [2, 6], 8: [2, 4], 9: [1, 3], 10: [2, 7], 11: [2, 8], 12: [2, 9]}
