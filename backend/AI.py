from backend.Node import Node
import math
class AI:
    root = None
    priorityMap = {} # Assigns weight to each node based on depth and children per node
    moveMap = {} # possible moves for each node
    def __init__(self,r):
        self.root = r
        print(self.moveMap)
    # @RN March 15 2016
    # Sets priority for each node based on depth / children of node
    # Nodes without children that are lower in the tree are prioritized higher than higher nodes with children
    def generatePriorityMap(self, root,depth=0):
        if root:
            self.priorityMap[root.ID] = (depth / (len(root.children) + 1))
            for ids, child in root.children.items():
                self.generatePriorityMap(child,depth+1)

    # @RN March 15 2016
    # Generates possible moves for each node based segmented by an angle
    def generateMoveMap(self, root, radius, degree=10, segments=0,radian=False):
        if not radian:
            degree = math.radians(degree)
        if segments == 0:
            segments = int(round(2*math.pi / degree,0))
        if root:
            self.moveMap[root.ID] = []
            for i in range(segments):
                self.moveMap[root.ID].append((round(root.x + radius*math.cos(i*degree),0),round(root.y +
                    radius*math.sin(i*degree),0)))
            for ids, child in root.children.items():
                self.generateMoveMap(child,radius,degree,segments,radian)

