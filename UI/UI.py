import pygame, sys, math
from pygame.locals import *

class UI:
    #fields
    boardSizeX = 0
    boardSizeY = 0
    windowSurface = None
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    def __init__(self, x,y):
        pygame.init()
        self.boardSizeX = x
        self.boardSizeY = y
        self.windowSurface = pygame.display.set_mode((self.boardSizeX,self.boardSizeY),0,32) #make 800x600 window
        self.windowSurface.fill(self.WHITE)
        pygame.display.update()  #draw the empty window

    def drawCircles(self,x,y,diameter):
        pygame.draw.arc(self.windowSurface,self.RED,(x-diameter/2,y-diameter/2,diameter,diameter),0,6.28,2);       

    def drawTree(self,root):
        if root:
            pygame.draw.circle(self.windowSurface,self.BLUE,(math.floor(root.x),math.floor(root.y)),5,0)
            for id,child in root.children.items():
                pygame.draw.aaline(self.windowSurface,self.RED,(math.floor(root.x),math.floor(root.y)),(math.floor(child.x),math.floor(child.y)),2)
                self.drawTree(child)

    def drawMidpoints(self,midpoints):
        if midpoints:
            for i in midpoints:
                root = midpoints[i]
                pygame.draw.circle(self.windowSurface,self.GREEN,(math.floor(root[0][0]),math.floor(root[1][0])),3,0)

