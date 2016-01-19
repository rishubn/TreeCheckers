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
class Player:
    _root = None
    _node = None # Node to change
    _clicked = False
    def __init__(self,root):
        self._root = root

    def update(self):
            if self._node is not None:
                self._node.x = pygame.mouse.get_pos()[0]
                self._node.y = pygame.mouse.get_pos()[1]
                


def main(player):
    event_loop(player)
    player.update()

def event_loop(player):
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            player._clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            player._clicked = False
            player._node = None
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif player._clicked == True:
            if player._node is None:
                try:
                    n = player._root.getNodeXY(event.pos,10)
                    if n is not None:
                         player._node = n
                except AttributeError:
                    n = None
        #if event.type == pygame.MOUSEBUTTONDOWN or player._clicked == True:
        #    n = player._root.getNodeXY(event.pos,10)
        #    if n is not None:
        #        player._node = player._root.getNodeXY(event.pos,10)
        #        print(player._node)
        #    if not player._clicked:
        #        player._clicked = True
        #    else:
        #        player._clicked = False


if __name__ == "__main__":
    board = BoardManager(100, 100, {'startDepth':2, 'numChildren':2},True)
    u = UI(None)
    board.positionMap = {}
    root = board.buildTree(2,2,board.getNextId())
    board.setIndexes(root,2)
    board.mapXY(root,2)
    u.drawTree(root)
    p = Player(root)
    clock = pygame.time.Clock()
    while 1:
        main(p)
        pygame.display.update()
        u.windowSurface.fill(u.WHITE)
        u.drawTree(root)
        clock.tick(60)
















