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
        self.collidableBlocks = pygame.sprite.Group()

    def loop(self):
        # Clear
        globs.character.collision()

        self.clearInGameLayers()
        self.screen.fill((0, 0, 0))

        # Background
        self.backgroundSurface.fill((100,120,200))
        self.worldSurface.fill((100,120,200))

        # Render, load & blit world
        self.worldSurface.blit(self.backgroundSurface, ((globs.resolution[0]/2)-globs.character.xy[0], (globs.resolution[1]/2)-globs.character.xy[1]))
        self.worldBlocks.draw(self.worldSurface)
        self.worldSurface.blit(globs.character.image, globs.character.xy)

        # Camera
        self.worldSurface.X = (globs.resolution[0]/2)-globs.character.xy[0]
        self.worldSurface.Y = (globs.resolution[1]/2)-globs.character.xy[1]

        # Make the camera not move when at edge of map
        extra = 100
        if self.worldSurface.X > 0+extra:
            self.worldSurface.X = 0+extra
        elif self.worldSurface.X < (globs.resolution[0]-globs.currentregion.pixelWidth)-extra:
            self.worldSurface.X = globs.resolution[0]-globs.currentregion.pixelWidth-extra
        if self.worldSurface.Y > 0+extra:
            self.worldSurface.Y = 0+extra
        elif self.worldSurface.Y < (globs.resolution[1]-globs.currentregion.pixelHeight)-extra:
            self.worldSurface.Y = (globs.resolution[1]-globs.currentregion.pixelHeight)-extra


        self.screen.blit(self.worldSurface, (self.worldSurface.X, self.worldSurface.Y))
        self.screen.blit(self.guiSurface, (0, 0))

    def loadRegion(self, regionname, spawnCoordinates=None):
        world, region = regionname.split('_')
        globs.currentregion = eval(world + '.' + region + '()')
        print(globs.currentregion.spawnCoordinates)

        self.backgroundSurface = Surface((globs.resolution[0], globs.resolution[1]))
        self.worldSurface = Surface((globs.currentregion.pixelWidth, globs.currentregion.pixelHeight), transparent=True)
        self.guiSurface = Surface((globs.resolution[0], globs.resolution[1]))

        rowcount = 1
        for row in globs.currentregion:
            columncount = 1
            for tile in row:
                if tile != "   ":
                    #print("tileid: {id}, xy: {xy}".format(id=tile, xy=blockPixel(columncount, rowcount)))
                    thisTile = eval('Block_{id}({xy})'.format(id=tile, xy=blockPixel(columncount, rowcount)))
                    self.worldBlocks.add(thisTile)
                columncount += 1
            rowcount += 1

        print(blockPixel(globs.currentregion.spawnCoordinates[0], globs.currentregion.spawnCoordinates[1]))
        globs.character.xy = blockPixel(globs.currentregion.spawnCoordinates[0], globs.currentregion.spawnCoordinates[1])
        #if not spawnCoordinates:
        #    globs.character.xy = blockPixel(globs.currentregion.spawnCoordinates[0], globs.currentregion.spawnCoordinates[1])
        #else:
        #    globs.character.xy = blockPixel(globs.currentregion.spawnCoordinates[0], globs.currentregion.spawnCoordinates[1])

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