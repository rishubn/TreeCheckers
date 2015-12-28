import pygame, sys
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
        for x in range(0,len(self.nodes)):   #draw the nodes and update after each one
            pygame.draw.circle(self.windowSurface, (255,0,0), self.nodes[x],20,0)
            pygame.display.update()

    def updateBoard(self, p1New, p2New):
        #play animations and whatnot as approprate

        #set new board
        p1Node = p1New
        p2Node = p2New


            

    
