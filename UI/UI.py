import pygame, sys, math
from pygame.locals import *

class UI:
    #fields
    p1Node = None
    p2Node = None
    windowSurface = None
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    def __init__(self, p1Node, p2Node):
        pygame.init()
        self.p1Node = p1Node
        self.p2Node = p2Node
        self.windowSurface = pygame.display.set_mode((800,600),0,32) #make 800x600 window
        self.windowSurface.fill(self.WHITE)
        pygame.display.update()  #draw the empty window
        
    def drawCircles(self):
        self.printed = set()
        self.printed.add(self.p1Node)
        self.drawTeamCircles(self.p1Node)
        self.printed.add(self.p2Node)
        self.drawTeamCircles(self.p2Node)        

    def drawTree(self,root):
        print(root.ID)
        if root:
            pygame.draw.circle(self.windowSurface,self.BLUE,(math.floor(root.x),math.floor(root.y)),5,0)
            for id,child in root.children.items():
                pygame.draw.line(self.windowSurface,self.RED,(math.floor(root.x),math.floor(root.y)),(math.floor(child.x),math.floor(child.y)),2)
                self.drawTree(child)
        pygame.display.update()


    """
    Draws all the circles below the given Node. If the given node is the root of a team, this function will draw every node on that team.
    """
    def drawTeamCircles(self, root):
        pygame.draw.circle(self.windowSurface, self.BLUE, (math.floor(root.x), math.floor(root.y)),2,0)
        pygame.display.update() #perhaps update should just be called once, at the end of this method? -Forrest Dec 29 2015
        for childID in root.children:
            if childID not in self.printed:
                self.printed.add(childID)
                self.drawTeamCircles(root.getChild(childID))

    def updateBoard(self, p1New, p2New):
        #play animations and whatnot as approprate

        #set new board
        self.p1Node = p1New
        self.p2Node = p2New


            

    
