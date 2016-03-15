import pytest, math, numpy
from backend.AI import AI
from backend.Node import Node
def testGenerateMoveMap():
    root = Node(50,50,0)
    degree = 90
    expected = {0:[(100,50),(50,100),(0,50),(50,0)]}
    a = AI(root)
    a.generateMoveMap(root,50,degree)
    assert expected == a.moveMap
