import pygame
from baseclasses import Surface
from .worlds import *
from .worldblocks import *
import globals as globs

class Game():
    def __init__(self, screen):
        self.screen = screen

        self.loadedTiles = {}
        self.worldBlocks = pygame.sprite.Group()
        self.loadRegion()

        self.backgroundSurface = Surface((globs.resolution[0], globs.resolution[1]))
        self.worldSurface = Surface((globs.currentregion.pixelWidth, globs.currentregion.pixelHeight))
        self.guiSurface = Surface((globs.resolution[0], globs.resolution[1]))

    def loop(self):
        # Clear
        self.clearInGameLayers()
        self.screen.fill((0, 0, 0))

        # Background
        self.backgroundSurface.fill((100,120,200))

        # Render, load & blit world
        #self.blitRegion()
        self.worldBlocks.draw(self.worldSurface)
        self.worldSurface.blit(globs.character.image, globs.character.xy)

        # Finish
        self.worldSurface.X = (globs.resolution[0]/2)-globs.character.xy[0]
        self.worldSurface.Y = (globs.resolution[1]/2)-globs.character.xy[1]

        extra = 100

        if self.worldSurface.X > 0+extra:
            #print("min x:{}".format(self.worldSurface.X))
            self.worldSurface.X = 0+extra
        elif self.worldSurface.X < (globs.resolution[0]-globs.currentregion.pixelWidth)-extra:
            #print("max x:{}".format(self.worldSurface.X))
            self.worldSurface.X = globs.resolution[0]-globs.currentregion.pixelWidth-extra
        if self.worldSurface.Y > 0+extra:
            #print("min Y:{}".format(self.worldSurface.Y))
            self.worldSurface.Y = 0+extra
        elif self.worldSurface.Y < (globs.resolution[1]-globs.currentregion.pixelHeight)-extra:
            #print("max Y:{}".format(self.worldSurface.Y))
            self.worldSurface.Y = (globs.resolution[1]-globs.currentregion.pixelHeight)-extra

        backgroundX = 0
        backgroundY = 0
        if backgroundX < self.worldSurface.X:
            backgroundX = self.worldSurface.X
        elif self.worldSurface.X-globs.resolution[0] < -globs.currentregion.pixelWidth:
            pass
            #backgroundX = -globs.currentregion.pixelWidth
        if backgroundY < self.worldSurface.Y:
            backgroundY = self.worldSurface.Y
        elif self.worldSurface.Y-globs.resolution[1] < -globs.currentregion.pixelHeight:
            pass
            #backgroundY = -globs.currentregion.pixelHeight

        self.screen.blit(self.backgroundSurface, (backgroundX, backgroundY))
        self.screen.blit(self.worldSurface, (self.worldSurface.X, self.worldSurface.Y))
        self.screen.blit(self.guiSurface, (0, 0))

    def loadRegion(self, spawnCoordinates=None):
        globs.currentregion = world1.TestRegion()

        rowcount = 1
        for row in globs.currentregion:
            columncount = 1
            for tile in row:
                if tile != "  ":
                    thisTile = eval('Block_{id}({xy})'.format(id=tile, xy=blockPixel(columncount, rowcount)))
                    self.worldBlocks.add(thisTile)
                    print("tileid: {id}, xy: {xy}".format(id=tile, xy=thisTile.xy))
                columncount += 1
            rowcount += 1


        if not spawnCoordinates:
            globs.character.xy = blockPixel(globs.currentregion.spawnCoordinates[0], globs.currentregion.spawnCoordinates[1])
        else:
            globs.character.xy = globs.currentregion.spawnCoordinates

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