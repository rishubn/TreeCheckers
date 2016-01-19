import math, numpy
class Node:
    loc = None
    ID = None
    children = {}
    def __init__(self, x, y, ID, children = None):
        self.loc = numpy.array([[x],[y]])
        self.loc.setflags(write = True)
        self.ID = ID
        self.children = {} if children is None else children #stupidly, just making {} be the default argument in the header causes all nodes to have the same list of children.

    @property
    def x(self):
        return self.loc[0][0]
    @x.setter
    def x(self, x):
        self.loc[0][0] = x
        #self.loc = numpy.array([[x],[self.loc[1][0]]])

    @property
    def y(self):
        return self.loc[1][0]
    @y.setter
    def y(self, y):
        self.loc[1][0] = y
        #self.loc = numpy.array([[self.loc[0][0]], [y]])
    

    #Take a Node and add it to the list of children
    def addChild(self, child):
        try:
            self.children[child.ID] = child
        except AttributeError:
            raise TypeError('''
                            the addChild function requires an object with an attribute named 
                            'ID', but it was passed an object of type {0} which has no 'ID' attribute.
                            '''.format(type(child)))

    ''' Gets the child of thise node with the matching ID. 
        If there is no such child this will return None
    '''
    def getChild(self, ID):
        return self.children.get(ID)

    """
    @FCC Jan 6 2016
    #maybe we should get rid of usage 2? -FCC Jan 6 2016
    usage 1: for some node r, if you want to search its children for a node with id foo, you can do
            r.getNode(foo)
    usage 2: for some node r, if you want to search its children for a node with id foo, you can do
            n.getNode(foo, root = r)
            where n is any node at all. 
    """
    def getNode(self, ID, root = None, default = None):
        if root == None:
            root = self
        if root.ID == ID:
            return root
        elif root.children is not None:
            for childID in root.children:
                output = (root.getChild(childID)).getNode(ID)
                if output is not None:
                    return output
        return default
        
    #pos is a tuple or list containing x at index 0 and y at index 1. radius is a positive number. Default can be anything. dist is a function that takes four numbers and returns one number.
    #finds the closest node in the given tree to pos that is within radius. returns default if there is no such node.
    def getNodeXY(self, pos, radius, root = None, default = None, dist = lambda x1,y1,x2,y2: math.sqrt((x1 - x2)**2 + (y1 - y2)**2)):
        minNode = default
        minDist = 9999999999
        if root == None:
            root = self
        if dist(root.x, root.y, pos[0], pos[1]) <= radius:
            minNode = self
            minDist = dist(root.x, root.y, pos[0], pos[1])
        elif root.children is not None:
            for childID in root.children:
                output = (root.getChild(childID)).getNodeXY(pos,radius)
                if output is not None and dist(output.x, output.y, pos[0], pos[1]) < minDist:
                    minNode = output
                    minDist = dist(output.x, output.y, pos[0], pos[1])
        return minNode

    #returns a list containing every node that evaluates to true under filterFunc. 
    def filterNodes(self, root = None, filterFunc = lambda X: X is not None):
        output = []
        if root is None:
            root = self
        if filterFunc(root):
            output.append(root)
        for childID in root.children:
            output.extend(self.filterNodes(root = root.children[childID], filterFunc = filterFunc))
        return output

    def __eq__(self, other):
        try:
            return self.ID == other.ID and numpy.allclose(self.loc, other.loc)
        except AttributeError: #if it doesn't talk like a duck or doesn't walk like a duck or something like that, it's probably not the duck we're looking for
            return False
    def __ne__(self, other):
        try:
            return self.ID != other.ID or not numpy.allclose(self.loc, other.loc)
        except AttributeError: #if it doesn't talk like a duck or doesn't walk like a duck or something like that, it's probably not the duck we're looking for
            return True
