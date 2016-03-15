from backend.BoardManager import BoardManager
from backend.AI import AI
from UI.UI import UI
import pygame, sys
from pygame.locals import *
import random


# oh no global variables!!
nodet = None
board = None
u = None
p1Move = True

def init():
    global board
    global u
    u = UI()
    board = BoardManager(u.configs['width'], u.configs['height'], {'startDepth':u.configs['depth'], 'numChildren':u.configs['numChildren'], 'maxDistance':50, 'numPlayers':2,'isRandom':u.configs['randomize']},True)


def drawOutline(player):
    if player["clicked"] == True and nodet is not None:
        u.drawCircles(player["node"][0],player["node"][1],board.maxDistance*2)
def updatePos(player, pos):
    if nodet:
        player["updateMidpoints"](nodet,[nodet.x,nodet.y,pos[0],pos[1]])
        nodet.x = pos[0]
        nodet.y = pos[1]

def main(player,ID):
    event_loop(player,ID)
    updatePos(player,pygame.mouse.get_pos())
    drawOutline(player)

def event_loop(player,ID):
    global nodet
    global p1Move
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            player["clicked"] = True
        elif event.type == pygame.MOUSEBUTTONUP:
            player["clicked"] = False
            if nodet:
                player["node"][2] = nodet.x
                player["node"][3] = nodet.y
                player["update"](ID,nodet.ID,player["node"])
                p1Move = not p1Move
                if not board.isValidMove(player["node"]):
                    p1Move = not p1Move
            nodet = None
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif player["clicked"] == True:
            if nodet is None:
                try:
                    nodet = player["root"].getNodeXY(event.pos,10)
                    player["node"] = [nodet.x,nodet.y,-1,-1]
                except AttributeError:
                    nodet = None
if __name__ == "__main__":
    init()
    board.buildPlayer()
    board.buildPlayer()
    clock = pygame.time.Clock()
    while 1:
        if p1Move:
            main(board.players[0],0)
        else:
            main(board.players[1],1)
        pygame.display.update()
        u.windowSurface.fill(u.WHITE)
        u.drawTree(board.players[0]["root"],u.PURPLE,u.RED)
        u.drawTree(board.players[1]["root"],u.BLUE,u.MAGENTA)
        u.drawMidpoints(board.midpoints,u.GREEN)
        clock.tick(60)
