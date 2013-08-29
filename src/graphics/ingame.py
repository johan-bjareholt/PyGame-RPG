import pygame
from .worlds import *
from .worldblocks import *
import globals as globs

class Game():
    def __init__(self, screen):
        self.screen = screen

        self.loadedTiles = {}
        self.loadRegion()

        # Create ingame layers
        self.backgroundSurface = pygame.Surface((globs.resolution[0], globs.resolution[1]))
        self.worldSurface = pygame.Surface((globs.currentregion.pixelWidth, globs.currentregion.pixelHeight))
        self.guiSurface = pygame.Surface((globs.resolution[0], globs.resolution[1]))

    def loop(self):
        # Clear
        self.clearInGameLayers()
        self.screen.fill((0, 0, 0))

        # Background
        self.backgroundSurface.fill((100,120,200))

        # Render, load & blit world
        self.blitRegion()
        self.worldSurface.blit(globs.character.image, globs.character.xy)

        # Finish
        gameX = (globs.resolution[0]/2)-globs.character.xy[0]
        gameY = (globs.resolution[1]/2)-globs.character.xy[1]

        extra = 100

        if gameX > 0+extra:
            #print("min x:{}".format(gameX))
            gameX = 0+extra
        elif gameX < (globs.resolution[0]-globs.currentregion.pixelWidth)-extra:
            #print("max x:{}".format(gameX))
            gameX = globs.resolution[0]-globs.currentregion.pixelWidth-extra
        if gameY > 0+extra:
            #print("min Y:{}".format(gameY))
            gameY = 0+extra
        elif gameY < (globs.resolution[1]-globs.currentregion.pixelHeight)-extra:
            #print("max Y:{}".format(gameY))
            gameY = (globs.resolution[1]-globs.currentregion.pixelHeight)-extra

        backgroundX = 0
        backgroundY = 0
        if backgroundX < gameX:
            backgroundX = gameX
        elif gameX-globs.resolution[0] < -globs.currentregion.pixelWidth:
            pass
            #backgroundX = -globs.currentregion.pixelWidth
        if backgroundY < gameY:
            backgroundY = gameY
        elif gameY-globs.resolution[1] < -globs.currentregion.pixelHeight:
            pass
            #backgroundY = -globs.currentregion.pixelHeight

        self.screen.blit(self.backgroundSurface, (backgroundX, backgroundY))
        self.screen.blit(self.worldSurface, (gameX, gameY))
        self.screen.blit(self.guiSurface, (0, 0))

    def loadRegion(self, spawnCoordinates=None):
        globs.currentregion = world1.TestRegion()

        if not spawnCoordinates:
            globs.character.xy = blockPixel(globs.currentregion.spawnCoordinates[0], globs.currentregion.spawnCoordinates[1])
        else:
            globs.character.xy = globs.currentregion.spawnCoordinates

    def blitRegion(self):
        rowcount = 1
        for row in globs.currentregion:
            tilecount = 1
            for tile in row:
                if tile != "  ":
                    if tile not in self.loadedTiles:
                        self.loadedTiles[tile] = eval('Block_'+tile+'()')
                        print('Loaded worldblock {}'.format(tile))
                    self.worldSurface.blit(self.loadedTiles[tile], (blockPixel(tilecount, rowcount)))
                tilecount += 1
            rowcount += 1

    def clearInGameLayers(self):
        # Clear default layers
        self.backgroundSurface.fill((255,0,255))
        self.backgroundSurface.set_colorkey((255,0,255))

        self.worldSurface.fill((255,0,255,0))
        self.worldSurface.set_colorkey((255,0,255))

        self.guiSurface.fill((255,0,255))
        self.guiSurface.set_colorkey((255,0,255))

def blockPixel(column, row):
    return (column*50-50, row*50-50)