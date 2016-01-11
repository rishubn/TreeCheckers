import pytest, math, numpy
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
	assert bm.makeMove(0, 0, 1 + bm.roots[0].x, 1 + bm.roots[0].y) #should return true because it was a valid move
def testMakeMoveInvalidInBounds():
	bm = BoardManager(1000, 1000, {'startDepth':2})
	assert not bm.makeMove(0, bm.roots[0].ID, 25 + bm.roots[0].x, 25 + bm.roots[0].y) #should return false because it was an invalid move because it was too far
def testmakeMoveInvalidOutOfBounds():
	bm = BoardManager(1000, 1000, {'startDepth':2})
	bm.roots[0].x = 1
	assert not bm.makeMove(0, 0, -2 + bm.roots[0].x, bm.roots[0].y) #should return false because it was an invalid move becuase it went outside the playing area

#test the _applyMove function
def test_ApplyMove():
	bm = BoardManager(1000, 1000, {'startDepth':1})
	bm._applyMove(bm.roots[0], -1, -2) #wouldn't be allowed if there was error checking
	assert bm.roots[0].x == -1 and bm.roots[0].y == -2

#test the isValidMove function
def testIsValidMoveValid():
	bm = BoardManager(1000, 1000, {'startDepth':1})
	assert bm.isValidMove(1, bm.roots[1].ID, bm.roots[1].x + 1, bm.roots[1].y + 1)
def testIsValidMoveInvalidTooFar():
	bm = BoardManager(1000, 1000, {'startDepth':1})
	assert not bm.isValidMove(1, bm.roots[1].ID, bm.roots[1].x + 10000, bm.roots[1].y + 10000)
def testIsValidMoveInvalidOutOfBounds():
	bm = BoardManager(1000, 1000, {'startDepth':1})
	assert not bm.isValidMove(1, bm.roots[1].ID, -100, bm.roots[1].y)

#test the rotation matrix function
def testRotMatrixtheq0():
	bm = BoardManager(1000, 1000)
	rm = numpy.array([[1,0],
					  [0,1]])
	assert numpy.allclose(bm.rotMatrix(0), rm)
def testRotMatrixRotatepi():
	bm = BoardManager(1000, 1000)
	rm = bm.rotMatrix(math.pi)
	vec = numpy.array([[1], [1]])
	assert numpy.allclose(rm.dot(vec), numpy.array([[-1.0], [-1.0]]))

#test the rotateTree function
def testRotateTreeCenter00():
	bm = BoardManager(1000, 1000, testing_mode = True)
	root = Node(0, 0, 0)
	bm.rotateTree(root, bm.rotMatrix(1))
	n = Node(0, 0, 0)
	assert numpy.allclose(root.loc, n.loc)
def testRotateTreeCenter11():
	bm = BoardManager(1000, 1000, testing_mode = True)
	root = Node(0, 0, 0)
	bm.rotateTree(root, bm.rotMatrix(math.pi), center = numpy.array([[1],[1]]))
	n = Node(2, 2, 2)
	assert numpy.allclose(root.loc, n.loc)

#test the buildTree function
#could really use some more tests, especially of correct placement of children, both in the tree and on the board
def testBuildTreeDepth1p0Node():
	bm = BoardManager(1000, 1000, {'startDepth':1, 'numChildren':1})
	assert bm.roots[0].ID is not None and bm.roots[0].x is not None and bm.roots[0].y is not None and len(bm.roots[0].children) == 1
def testBuildTreeDepth1p1Node():
	bm = BoardManager(1000, 1000, {'startDepth':1, 'numChildren':5})
	assert bm.roots[1].ID is not None and bm.roots[1].x is not None and bm.roots[1].y is not None and len(bm.roots[1].children) == 5
def testBuildTreeDepth2Children():
	bm = BoardManager(1000, 1000, {'startDepth':2, 'numChildren':2})
	assert len((bm.roots[0].children[
            list(bm.roots[0].children.keys())[0]
            ]).children) == 2 and len((bm.roots[1].children[
            list(bm.roots[1].children.keys())[0]]).children) == 2

#test doesKill function
def testDoesKillDoes():
	bm = BoardManager(1000,1000, {'startDepth':1, 'numChildren':1})
	victim = Node(1, 1, 1)
	root = Node(0, 0, 0, {victim.ID: victim})
	killer = Node(0, 1, 2)
	newX = 1
	newY = 0
	assert bm.doesKill(killerNode = killer, victimNode = victim, victimParent = root, newX = newX, newY = newY)
def testDoesKillDoesnt():
	bm = BoardManager(1000,1000, {'startDepth':1, 'numChildren':1})
	victim = Node(1, 1, 1)
	root = Node(0, 0, 0, {victim.ID: victim})
	killer = Node(0, 1, 2)
	newX = 0
	newY = 2
	assert not bm.doesKill(killerNode = killer, victimNode = victim, victimParent = root, newX = newX, newY = newY)

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
