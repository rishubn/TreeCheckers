class Node:
    x = None
    y = None
    id = None
    children = {}
    def __init__(self, x, y, id, children = {}):
        self.x = x
        self.y = y
        self.id = id
        self.children = children

    ''' Take a Node and add it to the list of children
     
    '''
    def addChild(self, child):
        try:
            self.children[child.id] = child
        except AttributeError:
            raise TypeError('''
                            the addChild function requires an object with an attribute named 
                            'id', but it was passed an object of type {0} which has no 'id' attribute.
                            '''.format(type(child)))

    ''' Gets the child of thise node with the matching id. 
        If there is no such child this will return None
    '''
    def getChild(self, id):
        return self.children.get(id)
        
