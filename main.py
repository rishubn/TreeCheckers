from BoardManager import BoardManager
from UI import UI
import pygame, sys
from pygame.locals import *
import random
'''
#generate 10 nodes at random xy's
nodes = list()
for x in range(0,10):
    nodes.append((random.randint(0,800),random.randint(0,600)))

#print their coordinates
print(*nodes,sep='\n')
'''
board = BoardManager(1000, 1000, {})
ui = UI(board.p1Node, board.p2Node)


#gameloop
while(True):
    x.drawCircles()
    while True:  #quit event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if board.newBoardState:
        	ui.updateBoard(board.p1Node, board.p2Node)

