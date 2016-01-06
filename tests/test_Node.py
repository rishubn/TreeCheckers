import pytest, math
from backend.Node import Node

#test the getNode function
def testGetNode():
	n0 = Node(0, 0, 0)
	n1 = Node(1, 1, 1)
	n2 = Node(2, 2, 2)
	n3 = Node(3, 3, 3)
	n0.addChild(n1)
	n0.addChild(n3)
	n1.addChild(n2)
	for childID in n1.children:
		print childID
	output = n0.getNode(2)
	assert output == n2

def testGetNode2():
	n0 = Node(0, 0, 0)
	n1 = Node(1, 1, 1)
	n2 = Node(2, 2, 2)
	n3 = Node(3, 3, 3)
	n0.addChild(n1)
	n1.addChild(n3)
	n1.addChild(n2)
	output = n0.getNode(2, root = n0)
	assert output == n2