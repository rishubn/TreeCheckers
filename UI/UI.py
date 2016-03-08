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
    YELLOW = (255, 255, 0)
    MAGENTA = (255, 0, 255)
    GREEN = (0, 255, 0)
    CYAN = (0,255,255)
    BLUE = (0, 0, 255)
    PURPLE = (128, 0, 128)

    def __init__(self, x,y):
        pygame.init()
        self.boardSizeX = x
        self.boardSizeY = y
        self.windowSurface = pygame.display.set_mode((self.boardSizeX,self.boardSizeY),0,32) #make 800x600 window
        self.windowSurface.fill(self.WHITE)
        pygame.display.update()  #draw the empty window

    def drawCircles(self,x,y,diameter):
        pygame.draw.arc(self.windowSurface,self.RED,(x-diameter/2,y-diameter/2,diameter,diameter),0,6.28,2);       

    def drawTree(self,root,circleColor, lineColor):
        if root:
            pygame.draw.circle(self.windowSurface,circleColor,(math.floor(root.x),math.floor(root.y)),5,0)
            for id,child in root.children.items():
                pygame.draw.aaline(self.windowSurface,lineColor,(math.floor(root.x),math.floor(root.y)),(math.floor(child.x),math.floor(child.y)),2)
                self.drawTree(child,circleColor,lineColor)

    def drawMidpoints(self,midpoints,color):
        if midpoints:
            for i in midpoints:
                root = midpoints[i]
                pygame.draw.circle(self.windowSurface,color,(math.floor(root[0][0]),math.floor(root[1][0])),3,0)

