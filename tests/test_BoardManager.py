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

#test the getNode function
def testGetNode():
	bm = BoardManager(1000, 1000, {})
	n0 = Node(0, 0, 0)
	n1 = Node(1, 1, 1)
	n2 = Node(2, 2, 2)
	n0.addChild(n1)
	n1.addChild(n2)
	assert bm.getNode(n0, 2) == n2

#test the makeMove function
def testMakeMoveValid():
	bm = BoardManager(1000, 1000, {'startDepth':2})
	assert bm.makeMove(1, 0, 1 + bm.p1Node.x, 1 + bm.p1Node.y) #should return true because it was a valid move
def testMakeMoveInvalidInBounds():
	bm = BoardManager(1000, 1000, {'startDepth':2})
	assert not bm.makeMove(1, bm.p1Node.id, 25 + bm.p1Node.x, 25 + bm.p1Node.y) #should return false because it was an invalid move because it was too far
def testmakeMoveInvalidOutOfBounds():
	bm = BoardManager(1000, 1000, {'startDepth':2})
	bm.p1Node.x = 1
	assert not bm.makeMove(1, 0, -2 + bm.p1Node.x, bm.p1Node.y) #should return false because it was an invalid move becuase it went outside the playing area

#test the _applyMove function
def test_ApplyMove():
	bm = BoardManager(1000, 1000, {'startDepth':0})
	bm._applyMove(bm.p1Node, -1, -2) #wouldn't be allowed if there was error checking
	assert bm.p1Node.x == -1 and bm.p1Node.y == -2

#test the isValidMove function
def testIsValidMoveValid():
	bm = BoardManager(1000, 1000, {'startDepth':0})
	assert bm.isValidMove(2, bm.p2Node.id, bm.p2Node.x + 1, bm.p2Node.y + 1)
def testIsValidMoveInvalidTooFar():
	bm = BoardManager(1000, 1000, {'startDepth':0})
	assert not bm.isValidMove(2, bm.p2Node.id, bm.p2Node.x + 10000, bm.p2Node.y + 10000)
def testIsValidMoveInvalidOutOfBounds():
	bm = BoardManager(1000, 1000, {'startDepth':0})
	assert not bm.isValidMove(1, bm.p1Node.id, -100, bm.p1Node.y)


#test the buildTree function
#could really use some more tests, especially of correct placement of children, both in the tree and on the board
def testBuildTreeDepth0p1Node():
	bm = BoardManager(1000, 1000, {'startDepth':0})
	assert bm.p1Node == Node(bm.boardSizeX / 8, bm.boardSizeY / 2, 0, {})
def testBuildTreeDepth0p2Node():
	bm = BoardManager(1000, 1000, {'startDepth':0})
	assert bm.p2Node == Node(bm.boardSizeX - (bm.boardSizeX / 8), bm.boardSizeY / 2, 1, {})
def testBuildTreeDepth1():
	bm = BoardManager(1000, 1000, {'startDepth':1, 'numChildren':2})
	assert len(bm.p1Node.children) == 2 and len(bm.p2Node.children) == 2
