import pygame, sys
from pygame.locals import *

class UI:
    #fields
    nodes = None
    windowSurface = None
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    def __init__(self,nodes):
        pygame.init();
        self.nodes = nodes;
        self.windowSurface = pygame.display.set_mode((800,600),0,32) #make 800x600 window
        self.windowSurface.fill(self.WHITE)
        pygame.display.update()  #draw the empty window
        
    def drawCircles(self):
        for x in range(0,len(self.nodes)):   #draw the nodes and update after each one
            pygame.draw.circle(self.windowSurface, (255,0,0), self.nodes[x],20,0)
            pygame.display.update()


            

    
