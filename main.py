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


nodet = None
def updatePos(player, pos):
    if nodet:
        print([nodet.x,nodet.y,pos[0],pos[1]])
        player["updateMidpoints"](nodet,[nodet.x,nodet.y,pos[0],pos[1]])
        nodet.x = pos[0]
        nodet.y = pos[1]
        
def main(player,ID):
    event_loop(player,ID)
    updatePos(player,pygame.mouse.get_pos())

def event_loop(player,ID):
    global nodet
    for event in pygame.event.get():
    #    print(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            player["clicked"] = True
        elif event.type == pygame.MOUSEBUTTONUP:
            player["clicked"] = False
            if nodet:
                player["node"][2] = nodet.x
                player["node"][3] = nodet.y
                player["update"](ID,nodet.ID,player["node"])
                print(player)
            nodet = None
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif player["clicked"] == True:
            if nodet is None:
                try:
                    nodet = player["root"].getNodeXY(event.pos,10)
                    player["node"] = [nodet.x,nodet.y,-1,-1]
                    print(player["node"])
                  #  if nodet is not None:
                        #player["node"] = nodet
                except AttributeError:
                    nodet = None
#test
if __name__ == "__main__":
    board = BoardManager(100, 100, {'startDepth':2, 'numChildren':2, 'maxDistance':50, 'numPlayers':1},True)
    u = UI(None)
    board.positionMap = {}
    
    root = board.buildTree(2,2,board.getNextId())
    board.setIndexes(root,2)
    board.mapXY(root,2)
    board.addPlayer(0,root)
    u.drawTree(root)
    board.buildMidpoints(root)
   # board.addPlayer(0,root)
    
    clock = pygame.time.Clock()
    while 1:
      #  print(board.players)
      #  print(board.roots)
        main(board.players[0],0)
        pygame.display.update()
        u.windowSurface.fill(u.WHITE)
        u.drawTree(board.players[0]["root"]) 
        u.drawMidpoints(board.midpoints)
        clock.tick(60)
















