import pygame, sys, math, os, pgu
from pygame.locals import *
from pgu import gui

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
    configs = {}
    def __init__(self):
        pygame.init()
        self.configs = self.startMenu()
        self.boardSizeX = self.configs['width']
        self.boardSizeY = self.configs['height']
        self.windowSurface = pygame.display.set_mode((self.boardSizeX,self.boardSizeY),0,32)
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

    def startMenu(self):
        configs = {}
        app = gui.Desktop()
        app.connect(gui.QUIT,app.quit,None)
        icon = pygame.image.load(os.path.join('assets','icon.png'))
        pygame.display.set_icon(icon)
        pygame.display.set_caption('TreeCheckers')
        c = gui.Table(width=400,height=300)
        #Intialize width box
        c.tr()
        c.td(gui.Label("Screen Width"))
        width = gui.Input(value='800',size=8)
        configs['width'] = 800
        def callback(e):
            try:
                configs['width'] = int(e.value)
            except:
                configs['width'] = 800
        width.connect(gui.CHANGE,callback,width)
        c.td(width,colspan=3)
        #initialize height box
        c.tr()
        c.td(gui.Label("Screen Height"))
        height = gui.Input(value='600',size=8)
        configs['height'] = 600
        def callback(e):
            try:
                configs['height'] = int(e.value)
            except:
                configs['height'] = 600
        height.connect(gui.CHANGE,callback,height)
        c.td(height,colspan=3)
        #Intialize depth select box
        c.tr()
        c.td(gui.Label("Tree depth"))
        depthSelect = gui.Select()
        depthSelect.add("2",'2')
        depthSelect.add("3",'3')
        depthSelect.add("4",'4')
        depthSelect.add("5",'5')
        depthSelect.value = '3'
        def callback(e):
            configs['depth'] = int(e.value)
            print(configs)
        depthSelect.connect(gui.CHANGE,callback,depthSelect)
        c.td(depthSelect,colspan=3)
        configs['depth'] = 3
        #Intialize children select box
        c.tr()
        c.td(gui.Label("Number of children per node"))
        numChildren = gui.Select()
        numChildren.add("2",'2')
        numChildren.add("3",'3')
        numChildren.add("4",'4')
        numChildren.add("5",'5')
        numChildren.value = '3'
        def callback(e):
            configs['numChildren'] = int(e.value)
            print(configs)
        numChildren.connect(gui.CHANGE,callback,numChildren)
        c.td(numChildren,colspan=3)
        configs['numChildren'] = 3
        #Initialize randomize select box
        c.tr()
        c.td(gui.Label("Randomize Trees"))
        randomizeOption = gui.Switch(False)
        c.td(randomizeOption,colspan=3)
        configs['randomize'] = False
        def callback(e):
            configs['randomize'] = bool(e.value)
            print(configs)
        randomizeOption.connect(gui.CHANGE,callback,randomizeOption)
        #Initialize start button
        c.tr()
        startButton = gui.Button("Start!")
        def callback():
            app.quit()
        startButton.connect(gui.CLICK, callback)
        c.td(startButton,colspan=3)
        app.run(c)
        return configs
