from backend.BoardManager import BoardManager
from UI.UI import UI
import pygame, sys
from pygame.locals import *
import random



nodet = None
board = None
u = None

def init():
    global board
    global u
    board = BoardManager(800, 300, {'startDepth':2, 'numChildren':2, 'maxDistance':50, 'numPlayers':1},True)
    u = UI(800,600)

def drawOutline(player):
    if player["clicked"] == True and nodet is not None:
        u.drawCircles(player["node"][0],player["node"][1],100)
def updatePos(player, pos):
    if nodet:
        print([nodet.x,nodet.y,pos[0],pos[1]])
        player["updateMidpoints"](nodet,[nodet.x,nodet.y,pos[0],pos[1]])
        nodet.x = pos[0]
        nodet.y = pos[1]

def main(player,ID):
    event_loop(player,ID)
    updatePos(player,pygame.mouse.get_pos())
    drawOutline(player)

def event_loop(player,ID):
    global nodet
    for event in pygame.event.get():
    #    print(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            player["clicked"] = True
        elif event.type == pygame.MOUSEBUTTONUP:
            player["clicked"] = False
            if nodet:
                #dont ask why these assignments work - @RN
                #player["node"][0] = nodet.x
                #player["node"][1] = nodet.y
                player["node"][2] = nodet.x
                player["node"][3] = nodet.y
                player["update"](ID,nodet.ID,player["node"])
                print("test")
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
    init()
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
