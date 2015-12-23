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

    /* Take a Node and add it to the list of children
     *
     */
    def addChild(self, child):
        children[child.id] = child

    /* Gets the child of thise node with the matching id. 
     * If there is no such child this will throw a keyerror.
     */
    def getChild(self, id):
        return children[id]
        
