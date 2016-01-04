import math
from backend.Node import Node

class BoardManager:
    boardSizeX = None
    boardSizeY = None
    p1Node = None
    p2Node = None
    _next_id = -1

    #flags
    newBoardState = False
    
    #config settings
    maxDistance = -1
    distanceMetric = 'euclidean'
    numChildren = -1

    ''' for best results, boardSizeX and boardSizeY should be positive integers, and configs should be a dictionary
      __init__ will use default values if configs does not contain necessary information
    '''
    #TODO remove checked from everywhere
    def __init__(self, boardSizeX, boardSizeY, configs = {}):
        self.boardSizeX = boardSizeX
        self.boardSizeY = boardSizeY
        
        #interpret configs dict
        self.maxDistance = configs.get('maxDistance', 25)
        self.distanceMetric = configs.get('distanceMetric', 'euclidean')
        self.numChildren = configs.get('numChildren', 3)        
        self.depth = configs.get('startDepth', 3)

        #build board
#        self.p1Node = self.buildTree(1, self.boardSizeX / 8, self.boardSizeY / 2, 0, self.boardSizeY, self.depth, self.numChildren)
 #       self.p2Node = self.buildTree(2, self.boardSizeX - (self.boardSizeX / 8), self.boardSizeY / 2, 0, self.boardSizeY, self.depth, self.numChildren)

        self.checked = set() #done to prevent buggy trees from causing infinite recursion. should be temporary
    
    #@FCC Jan 4 2016
    #Recursively builds tree, IDs in preorder
    def buildTree(self,depth, numChildren, lastid):
        children = {}
        if depth > 0:
            for i in range(0,numChildren):
                thisid = self.getNextId()
                children[thisid] = self.buildTree(depth-1,numChildren,thisid)
        return Node(None,None,lastid,children)






    #this code is from before a refactoring effort. It has since turned into three functions, 
    #isValidMove,
    #_applyMove, and
    #makeMove, 
    #to provide error checking functionality to someone who is considering making a move but hasn't decided yet. 
    #If everything is working fine with the running version of makeMove you can just delete all this stuff. 
    #commented on 1/1/2016 
    """
    ''' Takes the id of the node being moved, its new x location and its new y location
      returns True if the move was valid and False if it was invalid. 
      if the move is valid, updates the board and sets the newBoardState flag to True
    '''
    def makeMove(self,pnum, id, newX, newY):
        result = False
        self.checked = set()
        if pnum == 1:
            actingNode = self.getNode(self.p1Node, id)
        else:
            actingNode = self.getNode(self.p2Node, id)

        if self.getDistance(actingNode.x, actingNode.y, newX, newY) <= self.maxDistance:
            actingNode.x = newX
            actingNode.y = newY
            result = True

        if result == True:
            self.newBoardState = True

        return result
    """
    ''' Takes the id of the node being moved, its new x location and its new y location
      returns True if the move was valid and False if it was invalid. 
      if the move is valid, updates the board and sets the newBoardState flag to True
    '''
    def makeMove(self,pnum, id, newX, newY):
        self.checked = set()
        if pnum == 1:
            actingNode = self.getNode(self.p1Node, id)
        else:
            actingNode = self.getNode(self.p2Node, id)

        result = self.isValidMove(pnum, id, newX, newY)
        if result:
            self._applyMove(actingNode, newX, newY)
        return result

    '''
    Takes a node, and where it might be moved to, and checks if the move is valid. Returns True if it is, False otherwise
    '''
    def isValidMove(self, pnum, id, newX, newY):
        self.checked = set()
        if pnum == 1:
            actingNode = self.getNode(self.p1Node, id)
        else:
            actingNode = self.getNode(self.p2Node, id)
        return (newX >= 0 and 
                newY >= 0 and 
                newX <= self.boardSizeX and 
                newY <= self.boardSizeY and 
                self.getDistance(actingNode.x, actingNode.y, newX, newY) <= self.maxDistance)

    '''
    Takes a node and moves it. Also informs everyone that the board has changed. there is absolutely no error checking here, so only use this if you've done your error checking!
    If you want to make a move with error checking (i.e. only make the move if it's valid) use the makeMove function. 
    '''
    def _applyMove(self, actingNode, newX, newY):
        actingNode.x = newX
        actingNode.y = newY

        self.newBoardState = True

    """
    using checked to prevent infinite recursion here is necessary becuase buildTree is wrong, not because getNode is wrong (we think)
    """
    def getNode(self,root, id, default = None):
        if root.id == id:
            return root
        elif root.children is not None:
            for childID in root.children:
                if childID not in self.checked:
                    self.checked.add(childID)
                    output = self.getNode(root.getChild(childID), id)
                    if output is not None:
                        return output
        return default

    def getNextId(self):
        self._next_id += 1
        return self._next_id

    # Once we get support for different distance metrics, this function should compute the appropraite one based on distanceMetric
    def getDistance(self,x1, y1, x2, y2):
        return math.hypot(x2 - x1, y2 - y1) #math.hypot(x, y) returns math.sqrt(x^2, y^2)

    def getNodeDistance(self,n1, n2):
        if n1 is None:
            return self.getDistance(0, 0, n2.x, n2.y)
        elif n2 is None:
            return self.getDistance(n1.x, n1.y, 0, 0)
        else:
            return self.getDistance(n1.x, n1.y, n2.x, n2.y)
