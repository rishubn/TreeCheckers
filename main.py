from backend.BoardManager import BoardManager
from UI.UI import UI
import pygame, sys
from pygame.locals import *
import random

#this is a convenient pair of functions for printing the board state to console. 
#use if you want some debug info
def debugPrintBoardInfo(bm):
	for i in range(0, len(bm.roots)):
		print ("--------------------\n" +
		  	   "--------------------\n" +
		   	   "--------------------\n" +
		   	   "Player {0}:\n".format(i))
		debugPrintHelper(bm.roots[i])

def debugPrintHelper(root, formatString = ""):
	print("""{0}ID: {1}\n
			 {0}x: {2}\n
			 {0}y: {3}\n""".format(formatString, root.ID if root.ID else "None", 
												 root.x if root.x else "None", 
												 root.y if root.y else "None"))
	for childID in root.children:
		debugPrintHelper(root.getChild(childID), formatString = formatString + "\t")

"""
#generate 10 roots at random xy's
roots = list()
for x in range(0,10):
    roots.append((random.randint(0,800),random.randint(0,600)))

#print their coordinates
print(*roots,sep='\n')
"""
board = BoardManager(1000, 1000, {'startDepth':2})
ui = UI(board.roots)
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
        	ui.updateBoard(board.roots)

