import math, numpy
from backend.Node import Node

class BoardManager:
    boardSizeX = None
    boardSizeY = None
    roots = []
    _next_id = -1
    midpoints = {} #every node except root should have one entry in this dict, key ID, value tuple containing x midpoint, y midpoint.
    
    #maps node ID to depth and index array
    positionMap = {}
    #flags
    newBoardState = False
    
    #config settings
    maxDistance = -1
    distanceMetric = ''
    numChildren = -1
    depth = -1
    numPlayers = -1

    ''' for best results, boardSizeX and boardSizeY should be positive integers, and configs should be a dictionary.
      __init__ will use default values if configs does not contain necessary information
    '''
    def __init__(self, boardSizeX, boardSizeY, configs = {}, testing_mode = False):
        self.boardSizeX = int(boardSizeX)
        self.boardSizeY = int(boardSizeY)
        
        #interpret configs dict
        self.maxDistance = configs.get('maxDistance', 25)
        self.distanceMetric = configs.get('distanceMetric', 'euclidean').lower()
        self.numChildren = int(configs.get('numChildren', 3))
        self.depth = int(configs.get('startDepth', 3))
        self.numPlayers = int(configs.get('numPlayers', 2))
        self.killRadius = int(configs.get('killRadius', 10))
        self.roots = [None] * self.numPlayers
        if self.depth < 1:
            self.depth = 1
        if self.numChildren < 1:
            self.numChildren = 1
        if self.killRadius < 0:
            self.killRadius = 0.1
        if not testing_mode:
            for i in range(0, self.numPlayers):
                #build board for player 
                self.positionMap = {} #must be before buildTree is called
                self.roots[i] = self.buildTree(self.depth, self.numChildren, self.getNextId())
                self.setIndexes(self.roots[i], self.numChildren)
                self.mapXY(self.roots[i], self.numChildren)
                r = 2 * math.pi * (i / self.numPlayers)
                self.rotateTree(self.roots[i], self.rotMatrix(r), center = numpy.array([[boardSizeX/2],[boardSizeY/2]]))
                self.buildMidpoints(self.roots[i])
    
    #@FCC Jan 13 2016
    #assemble a dict of midpoints for easier access during gameplay
    def buildMidpoints(self, root):
        for childID in root.children:
            self.midpoints[childID] = numpy.array([[(root.children[childID].x + root.x) / 2], [(root.children[childID].y + root.y) / 2]])
            self.buildMidpoints(root.children[childID])

    #root should be a Node, theta should be a float (in radians) and center should be a 
    def rotateTree(self, root, rm, center = numpy.array([[0],[0]])):
        root.loc = rm.dot(root.loc - center) + center
        for childID in root.children:
            self.rotateTree(root.children[childID], rm, center)

    #Argument is in Radians, not degrees
    #@FCC Jan 11 2016
    def rotMatrix(self, theta):
        return numpy.array([[math.cos(theta), -1 * math.sin(theta)],
                            [math.sin(theta),      math.cos(theta)]])
        
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
    # split into two loops, one to set indexes of a node's children, the second to traverse the tree
    # Ask Rishub for more information if confused
    # TODO write tests for this method
    def setIndexes(self,root,numChildren,parentindex=None):
        if root:
            if self.positionMap[root.ID][0] == 0 and self.positionMap[root.ID][1] == -1:
                parentindex = 1
                self.positionMap[root.ID][1] = parentindex
            i = numChildren -1
            for ids,child in root.children.items():
                index = parentindex * numChildren - i
                self.positionMap[child.ID][1] = index
                i = i - 1
                #print("ID: " + str(ids) + " parentindex: " + str(parentindex) + " numChildren: " + str(numChildren) + "index: " + str(index) + " i: " + str(i))

            for ids,child in root.children.items():
                self.setIndexes(child,numChildren,self.positionMap[child.ID][1])
    
    # @RN Jan 5 2016
    # maps positionMap to X and Ys relative to the board size for N children in a tree
    # ask Rishub for more info
    def mapXY(self, root, numChildren):
        for ids, positions in self.positionMap.items():
            depth = positions[0]
            index = positions[1]
            x = index * self.boardSizeX / (numChildren ** depth +1)
            y = depth * self.boardSizeY / self.depth
            actingNode = root.getNode(ids)
            actingNode.x = x
            actingNode.y = y+10
    
    ''' Takes the number of the player that owns the node being moved, the id of the node being moved, its new x location and its new y location
      returns True if the move was valid and False if it was invalid. 
      if the move is valid, updates the board and sets the newBoardState flag to True
    '''
    def makeMove(self, pnum, nodeId, newX, newY):
        try:
            actingNode = self.roots[pnum].getNode(nodeId)
        except IndexError:
            print ("""In makeMove:\n
                      Attempt to access nonexistent player root for player number {0} was made (there are only {1} players).\n
                      returning False and continuing execution.""".format(pnum, len(self.roots)))
            return False

        result = self.isValidMove(pnum, nodeId, newX, newY)
        if result:
            self._applyMove(actingNode, newX, newY)
            #code below commented purely because the functions getKillList, kill, and _killChild are untested. This *should* work just fine.
            killList = self.getKillList(pnum, numpy.array([[newX], [newY]]))
            #if the list is empty, it's False as far as the if statement is concerned
            if killList:
                for ID in killList:
                    self.kill(ID)
        return result

    
    #Takes a node, and where it might be moved to, and checks if the move is valid. Returns True if it is, False otherwise
    def isValidMove(self, pnum, nodeId, newX, newY):
        try:
            actingNode = self.roots[pnum].getNode(nodeId)
        except IndexError:
            print ("""In makeMove:\n
                      Attempt to access nonexistent player root for player number {0} was made (there are only {1} players).\n
                      returning False and continuing execution.""".format(pnum, len(self.roots)))
            return False

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
        #if the moving node is not a root node, then we need to update the midpoints dict also. 
        if not (actingNode.ID in map(lambda X: X.ID, self.roots)):
            #infer the location of the parent
            parentX = (self.midpoints[actingNode.ID][0][0] * 2) - actingNode.x
            parentY = (self.midpoints[actingNode.ID][1][0] * 2) - actingNode.y
            self.midpoints[actingNode.ID] = numpy.array([[(parentX + newX) / 2], [(parentY + newY) / 2]]) #update the midpoint appropriately

        #update the node itself
        actingNode.x = newX
        actingNode.y = newY

        self.newBoardState = True #notify UI
    
    #returns a list of ids of nodes that will be killed if any node owned by player pnum moves to pos.  
    #pnum is the number of the player who owns the moving node. x and y are the locations the node is moving to. 
    def getKillList(self, pnum, pos):
        r = [] 
        for i in range(0, len(self.roots)):
            if i != pnum:
                output = self.roots[i].filterNodes(filterFunc = lambda X: self.getDistance(X.x, X.y, pos[0], pos[1]) <= self.killRadius)
                output = map(lambda X: X.ID, output)
                r.extend(output)
        return r

    #warning: this function will immediately kill the specified node (if it exists), no matter what.
    #don't use it unless you're sure the node in question must die!
    def kill(self, ID, root = None):
        if root:
            rootList = [root]
        else:
            rootList = self.roots
        for root in rootList:
            self._killChild(ID, root)

    #warning: this function will immediately kill the specified node (if it is in root's tree), no matter what.
    #don't use it unless you're sure the node in question must die!
    def _killChild(self, ID, root):
        if ID in root.children:
            del root.children[ID]
            del self.midpoints[ID]
            return None #exit since we're done here
        #else
        for childID in root.children:
            self._killChild(ID, root.children[childID])

    #code is due to a misunderstanding about what causes a node to die. Don't delete it though, @FCC may post it online because it's actually kinda neat
    """
    #takes node, node, node, float, float. Indicates whether moving killerNode from its current location to newX, newY would cause victimNode to die.
    def doesKill(self, killerNode, victimNode, victimParent, newX, newY):
        #if the x intervals the line segments inhabit do not overlap
        if (min(killerNode.x, newX) > max(victimNode.x, victimParent.x) or min(victimNode.x, victimParent.x) > max(killerNode.x, newX)):
            print("earlyfalse")
            return False;
        # the intersection of the x intervals each of the line segments inhabit. If the location where the lines intersect
        # isn't in this interval, then the line segments don't intersect
        xInterval = (max(min(killerNode.x, newX), min(victimNode.x, victimParent.x)),
                     min(max(victimNode.x, victimParent.x), max(killerNode.x, newX)))
        #slope of the line that connects the victim and its parent
        vicSlope = (victimParent.y - victimNode.y) / (victimParent.x - victimNode.x)
        #slope of the line that connects the killer's old location and its new location
        kilSlope = (killerNode.y - newY) / (killerNode.x - newX)
        #y-intercept of the line that connects the victim and its parent
        vicIntercept = (-1 * vicSlope * victimNode.x) + victimNode.y
        #y-intercept of the line that connects the killer's old location and its new location
        kilIntercept = (-1 * kilSlope * newX) + newY
        #location on the x axis where the two lines intersect
        x = (vicIntercept - kilIntercept) / (kilSlope - vicSlope)

        return x >= xInterval[0] and x <= xInterval[1] 
    """
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
