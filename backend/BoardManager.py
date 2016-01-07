import math
from backend.Node import Node

class BoardManager:
    boardSizeX = None
    boardSizeY = None
    p1Node = None
    p2Node = None
    _next_id = -1
    
    #TODO to be moved to tree class
    #maps node ID to depth and index array
    positionMap = {}
    #flags
    newBoardState = False
    
    #config settings
    maxDistance = -1
    distanceMetric = ''
    numChildren = -1
    depth = -1

    ''' for best results, boardSizeX and boardSizeY should be positive integers, and configs should be a dictionary
      __init__ will use default values if configs does not contain necessary information
    '''
    #TODO remove checked from everywhere
    def __init__(self, boardSizeX, boardSizeY, configs = {}):
        self.boardSizeX = int(boardSizeX)
        self.boardSizeY = int(boardSizeY)
        
        #interpret configs dict
        self.maxDistance = configs.get('maxDistance', 25)
        self.distanceMetric = configs.get('distanceMetric', 'euclidean').lower()
        self.numChildren = int(configs.get('numChildren', 3))        
        self.depth = int(configs.get('startDepth', 3))
        if self.depth < 1:
            self.depth = 1

        #build board for player 1
        self.positionMap = {} #must be before buildTree is called
        self.p1Node = self.buildTree(self.depth, self.numChildren, self.getNextId())
        self.setIndexes(self.p1Node, self.numChildren)
        self.mapXY(self.p1Node, self.numChildren)
        #build board for player 2
        self.positionMap = {} #must be before buildTree is called
        self.p2Node = self.buildTree(self.depth, self.numChildren, self.getNextId())
        self.setIndexes(self.p2Node, self.numChildren)
        self.mapXY(self.p2Node, self.numChildren)
    
    # @FCC Jan 4 2016
    # Recursively builds tree, IDs in preorder
    def buildTree(self,depth, numChildren, lastid):
        children = {}
        if depth > 0:
            for i in range(0,numChildren):
                thisid = self.getNextId()
                children[thisid] = self.buildTree(depth-1,numChildren,thisid)
        self.positionMap[lastid] = [self.depth-depth,-1]
        return Node(None,None,lastid,children)

    # @RN Jan 5 2016
    # Recursively sets serial indexes into positionMap for tree with N children
    # index = parentindex * numchildren - lateral position in tree
    # split into two loops, one to set indexes of a nodes children, the second to traverse the tree
    # Ask Rishub for more information if confused
    # TODO write tests for this method
    def setIndexes(self,root,numChildren,parentindex=None):
        if root:
            if self.positionMap[root.ID][0] == 0 and self.positionMap[root.ID][1] == -1:
                parentindex = 1
                self.positionMap[root.ID][1] = parentindex
            i = numChildren-1
            for ids,child in root.children.items():
                index = parentindex * numChildren - i
                self.positionMap[child.ID][1] = index
                i = i - 1
            for ids,child in root.children.items():
                self.setIndexes(child,numChildren,self.positionMap[child.ID][1])
    
    # @RN Jan 5 2016
    # maps positionMap to X and Ys relative to the board size for N children in a tree
    # ask Rishub for more info
    def mapXY(self, root, numChildren):
        for ids, positions in self.positionMap.items():
            depth = positions[0]
            index = positions[1]
            x = index * self.boardSizeX / (2 ** depth + numChildren - 1)
            y = depth * self.boardSizeY / self.depth
            
            actingNode = root.getNode(ids)
            actingNode.x = x
            actingNode.y = y            
    
    # this code is from before a refactoring effort. It has since turned into three functions, 
    # isValidMove,
    # _applyMove, and
    # makeMove, 
    # to provide error checking functionality to someone who is considering making a move but hasn't decided yet. 
    # If everything is working fine with the running version of makeMove you can just delete all this stuff. 
    # commented on 1/1/2016 
    """
    ''' Takes the id of the node being moved, its new x location and its new y location
      returns True if the move was valid and False if it was invalid. 
      if the move is valid, updates the board and sets the newBoardState flag to True
    '''
    def makeMove(self,pnum, id, newX, newY):
        result = False
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
    def makeMove(self,pnum, nodeId, newX, newY):
        if pnum == 1:
            #actingNode = self.getNode(self.p1Node, nodeId)
            actingNode = self.p1Node.getNode(nodeId)
        else:
            #actingNode = self.getNode(self.p2Node, nodeId)
            actingNode = self.p2Node.getNode(nodeId)

        result = self.isValidMove(pnum, nodeId, newX, newY)
        if result:
            self._applyMove(actingNode, newX, newY)
        return result

    '''
    Takes a node, and where it might be moved to, and checks if the move is valid. Returns True if it is, False otherwise
    '''
    def isValidMove(self, pnum, nodeId, newX, newY):
        if pnum == 1:
            #actingNode = self.getNode(self.p1Node, id)
            actingNode = self.p1Node.getNode(nodeId)
        else:
            #actingNode = self.getNode(self.p2Node, id)
            actingNode = self.p2Node.getNode(nodeId)
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
