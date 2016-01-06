class Node:
    x = None
    y = None
    ID = None
    children = {}
    def __init__(self, x, y, ID, children = None):
        self.x = x
        self.y = y
        self.ID = ID
        self.children = {} if children is None else children #stupidly, just making {} be the default argument in the header causes all nodes to have the same list of children.

    ''' Take a Node and add it to the list of children
     
    '''
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
        
    def __eq__(self, other):
        try:
            return self.ID == other.ID and self.x == other.x and self.y == other.y
        except AttributeError: #if it doesn't talk like a duck or doesn't walk like a duck or something like that, it's probably not the duck we're looking for
            return False
    def __ne__(self, other):
        try:
            return self.ID != other.ID or  self.x != other.x or  self.y != other.y
        except AttributeError: #if it doesn't talk like a duck or doesn't walk like a duck or something like that, it's probably not the duck we're looking for
            return True