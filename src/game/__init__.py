import pygame
from graphics.baseclasses import Surface
from .worlds import *
from .worldblocks import *
import globals as globs

class Game():
    def __init__(self, screen):
        self.screen = screen

    def loop(self):
        # Clear
        globs.character.loop()

        self.blitBackground()

        cameraX = globs.character.xy[0]-(globs.resolution[0]/2)
        if cameraX < 0: cameraX = 0
        if cameraX > globs.currentregion.pixelWidth: cameraX = globs.currentregion.pixelWidth+(globs.resolution[0])
        cameraY = globs.character.xy[1]-(globs.resolution[1]/2)
        if cameraY < 0: cameraY = 0
        elif cameraY > globs.currentregion.pixelHeight: cameraY = globs.currentregion.pixelHeight+(globs.resolution[1])
        globs.cameraX, globs.cameraY = cameraX, cameraY

        columnstart = int(cameraX/50)
        columnend   = int(columnstart+2*(globs.resolution[1]/50))

        rowstart = int(cameraY/50)
        rowend   = int(rowstart+(globs.resolution[0]/50))
        #print("X:{} Y:{}".format(cameraX, cameraY))
        #print("Row: {},{} Column: {},{}".format(rowstart,rowend,columnstart,columnend))

        rowcount = rowstart
        for row in globs.currentregion.renderedmap[rowstart:rowend]:
            columncount = columnstart
            for tile in row[columnstart:columnend]:
                if tile:
                    self.screen.blit(tile.image, (tile.xy[0]-cameraX, tile.xy[1]-cameraY))
                    #print(str(tile.xy))
                    #print("Blitting {} on {}".format(tile, (tile.xy[0], tile.xy[1]) ))
                    #print("row: {} Column: {}".format(rowcount, columncount))
                columncount += 1
            rowcount += 1

        self.screen.blit(globs.character.image, (globs.character.xy[0]-(cameraX), globs.character.xy[1]-(cameraY)))

    def blitBackground(self):
        self.screen.blit(self.backgroundSurface, (0,0))


    def loadRegion(self, regionname, spawnCoordinates=None):
        # (Re)load tiles
        self.loadedTiles = {}

        # Load world
        world, region = regionname.split('_')
        globs.currentregion = eval(world + '.' + region + '()')
        print(globs.currentregion.spawnCoordinates)
        # Load world surfaces
        self.backgroundSurface = Surface((globs.resolution[0], globs.resolution[1]))
        self.backgroundSurface.fill((100,120,200))
        # Create/Clear sprite groups
        self.worldBlocks = pygame.sprite.Group()
        self.collidableBlocks = pygame.sprite.Group()
        ## Different entities
        # World entities
        self.worldEntitiyBlocks = pygame.sprite.Group()
        self.worldEntities = pygame.sprite.Group()
        # General Entities
        self.entities = pygame.sprite.Group()

        globs.currentregion.renderedmap = []

        # Blit blocks
        rowcount = 1
        for row in globs.currentregion:
            columncount = 1
            renderedRow = []
            for tile in row:
                if tile != "   ":
                    #print("tileid: {id}, xy: {xy}".format(id=tile, xy=blockPixel(columncount, rowcount)))
                    thisTile = eval('Block_{id}({xy})'.format(id=tile, xy=blockPixel(columncount, rowcount)))
                    renderedRow.append(thisTile)
                    self.worldBlocks.add(thisTile)
                else:
                    renderedRow.append("")
                columncount += 1
            globs.currentregion.renderedmap.append(renderedRow)
            rowcount += 1


        # Load worldentities
        for worldentity in globs.currentregion.entities:
            self.worldEntities.add(
                worldentity['entity'](self, blockPixel(worldentity['coords'][0], worldentity['coords'][1])))


        # Move character to spawncoords
        print(blockPixel(globs.currentregion.spawnCoordinates[0], globs.currentregion.spawnCoordinates[1]))
        globs.character.move(blockPixel(globs.currentregion.spawnCoordinates[0], globs.currentregion.spawnCoordinates[1]))


def blockPixel(column, row):
    return (column*50-50, row*50-50)