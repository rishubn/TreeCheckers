from BoardManager import BoardManager
from UI import UI
import pygame, sys
from pygame.locals import *
import random

#this is a convenient pair of functions for printing the board state to console. 
#use if you want some debug info
printed = set()
def debugPrintBoardInfo(bm):
	print ("--------------------\n"+
		   "--------------------\n"+
		   "--------------------\n"+
		   "Player 1:\n")
	printed.add(bm.p1Node.ID)
	debugPrintHelper("", bm.p1Node)
	print ("--------------------\n"+
		   "--------------------\n"+
		   "--------------------\n"+
		   "Player 2:\n")
	printed.add(bm.p2Node.ID)
	debugPrintHelper("", bm.p2Node)

def debugPrintHelper(formatString, root):
	print("{0}ID: {1}\n{0}x: {2}\n{0}y: {3}\n".format(formatString, root.ID, root.x, root.y))
	for childID in root.children:
		if childID not in printed:
			printed.add(childID)
			debugPrintHelper(formatString + "\t", root.getChild(childID))

"""
#generate 10 nodes at random xy's
nodes = list()
for x in range(0,10):
    nodes.append((random.randint(0,800),random.randint(0,600)))

#print their coordinates
print(*nodes,sep='\n')
"""
board = BoardManager(1000, 1000, {'startDepth':2})
ui = UI(board.p1Node, board.p2Node)
#debugPrintBoardInfo(board)

#gameloop
while True:
    ui.drawCircles() #maybe it should only draw if the board changes (i.e. immediately after update board, or even whenever updateBoard is called) -Forrest Dec 30 2015
    while True:  #quit event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if board.newBoardState:
        	ui.updateBoard(board.p1Node, board.p2Node)

