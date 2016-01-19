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
		print(childID)
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

#test filterNodes
def testFilterNodes():
	n0 = Node(0, 0, 0)
	n1 = Node(1, 1, 1)
	n2 = Node(2, 2, 2)
	n3 = Node(3, 3, 3)
	n0.addChild(n1)
	n1.addChild(n3)
	n1.addChild(n2)
	output = n0.filterNodes(filterFunc = lambda X: X.ID == 2)
	print(len(output))
	for n in output:
		print(n.ID)
	assert output == [n2]

#test the .x property setter
def testXSetterWithXGetter():
	n0 = Node(0, 0, 0)
	n0.x = 1
	assert n0.x == 1
def testXSetterWithLoc():
	n0 = Node(0, 0, 0)
	n0.x = 1
	print (n0.loc)
	assert n0.loc[0][0] == 1
#test the .y property setter
def testYSetterWithXGetter():
	n0 = Node(0, 0, 0)
	n0.y = 1
	assert n0.y == 1
def testYSetterWithLoc():
	n0 = Node(0, 0, 0)
	n0.y = 1
	print(n0.loc)
	assert n0.loc[1][0] == 1

#test the __eq()__ function
def testNodeEq():
	n0 = Node(0, 0, 0, {})
	n1 = Node(0, 0, 0, {})
	assert n0 == n1

#test the __ne()__ function
def testNodeNe():
	n0 = Node(0, 0, 0, {})
	n1 = Node(1, 1, 1, {})
	assert n0 != n1
