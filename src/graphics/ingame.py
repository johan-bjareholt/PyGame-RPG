import pygame
from .worlds import *
from .worldblocks import *
import globals as globs

class Game():
    def __init__(self, screen, world, region, spawnCoordinates=None):
        self.screen = screen
        self.world = world
        self.region = region

        print("Loading region " + self.region + " in " + self.world)
        global currentRegion, currentWorld
        #currentRegion = import_module(str("."+world), '.worlds')
        region = world1.StartRegion()
        currentRegion = region
        global loadedTiles
        self.loadedTiles = {}

        global regionHeight, regionWidth
        regionHeight = len(region)*50
        regionWidth  = len(region[0])*50

        if not spawnCoordinates:
            globs.character.xy = self.blockPixel(currentRegion.spawnCoordinates[0], currentRegion.spawnCoordinates[1])
        else:
            globs.character.xy = spawnCoordinates

        print("Loaded region {region} (spawn: {spawn}, height: {h}, width: {w})".format(region=self.region, spawn=currentRegion.spawnCoordinates, w=regionWidth, h=regionHeight))

        # Create ingame layers
        self.backgroundSurface = pygame.Surface((globs.resolution[0], globs.resolution[1]))
        self.worldSurface = pygame.Surface((regionWidth, regionHeight))
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
        elif gameX < (globs.resolution[0]-regionWidth)-extra:
            #print("max x:{}".format(gameX))
            gameX = globs.resolution[0]-regionWidth-extra
        if gameY > 0+extra:
            #print("min Y:{}".format(gameY))
            gameY = 0+extra
        elif gameY < (globs.resolution[1]-regionHeight)-extra:
            #print("max Y:{}".format(gameY))
            gameY = (globs.resolution[1]-regionHeight)-extra

        backgroundX = 0
        backgroundY = 0
        if backgroundX < gameX:
            backgroundX = gameX
        elif gameX-globs.resolution[0] < -regionWidth:
            pass
            #backgroundX = -regionWidth
        if backgroundY < gameY:
            backgroundY = gameY
        elif gameY-globs.resolution[1] < -regionHeight:
            pass
            #backgroundY = -regionHeight

        self.screen.blit(self.backgroundSurface, (backgroundX, backgroundY))
        self.screen.blit(self.worldSurface, (gameX, gameY))
        self.screen.blit(self.guiSurface, (0, 0))

    def blitRegion(self):
        rowcount = 1
        for row in currentRegion:
            tilecount = 1
            for tile in row:
                if tile != "  ":
                    if tile not in self.loadedTiles:
                        self.loadedTiles[tile] = eval('Block_'+tile+'()')
                        print('Loaded worldblock {}'.format(tile))
                    self.worldSurface.blit(self.loadedTiles[tile], (self.blockPixel(tilecount, rowcount)))
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

    def blockPixel(self, column, row):
        return (column*50-50, row*50-50)