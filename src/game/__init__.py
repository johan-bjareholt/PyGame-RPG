import pygame
from graphics.baseclasses import Surface, Sprite
from menu.baseclasses import TextBox
from .worlds import *
from .worldblocks import *
from .baseclasses import *
from .entities import BouncyBall, Zombie
import globals as globs


class GameClient():
    def __init__(self, screen):
        self.screen = screen
        self.gameserver = GameServer('world1')

    def loop(self):
        # Do actions before render
        for entity in self.entities:
            entity.events()
        #print(self.bouncyBall.speedY)
        #print(self.bouncyBall.Y)
        #globs.character.loop()

        '''
            Background and camera
        '''
        self.blitBackground()

        cameraX = globs.character.xy[0]-(globs.resolution[0]/2)
        if cameraX < 0: cameraX = 0
        if cameraX > globs.currentregion.pixelWidth-globs.resolution[0]: cameraX = globs.currentregion.pixelWidth-(globs.resolution[0])
        cameraY = globs.character.xy[1]-(globs.resolution[1]/2)
        if cameraY < 0: cameraY = 0
        elif cameraY > globs.currentregion.pixelHeight-globs.resolution[1]: cameraY = globs.currentregion.pixelHeight-(globs.resolution[1])
        globs.cameraX, globs.cameraY = cameraX, cameraY

        '''
            World
        '''

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
                    tile.blitDecoration((tile.xy[0]-cameraX, tile.xy[1]-cameraY))
                    #print(str(tile.xy))
                    #print("Blitting {} on {}".format(tile, (tile.xy[0], tile.xy[1]) ))
                    #print("row: {} Column: {}".format(rowcount, columncount))
                columncount += 1
            rowcount += 1

        '''
            Entities
        '''

        for entity in self.entities:
            entity.blit()


        '''
            Gui
        '''
        # Update chatbox

        # Update minimap
        self.miniMap.unscaledImage.fill((0,0,0))
        for row in globs.currentregion.renderedmap[rowstart:rowend]:
            columncount = columnstart
            for tile in row[columnstart:columnend]:
                if tile:
                    self.miniMap.unscaledImage.set_at((int((tile.xy[0]-cameraX)/50), int((tile.xy[1]-cameraY)/50)), tile.bgColor)
                    #self.screen.blit(tile.image, (tile.xy[0]-cameraX, tile.xy[1]-cameraY))
                columncount += 1
            rowcount += 1
        self.miniMap.image = pygame.transform.scale(self.miniMap.unscaledImage, (100, 100))

        # Blit add gui elements
        self.guiElements.draw(globs.screen)

    def blitBackground(self):
        self.screen.blit(self.backgroundSurface, (0,0))


    def loadRegion(self, regionname, spawnCoordinates=None):
        # (Re)load tiles
        self.loadedTiles = {}

        '''
            Background
        '''
        # Load world surfaces
        self.backgroundSurface = Surface((globs.resolution[0], globs.resolution[1]))
        self.backgroundSurface.fill((100,120,200))

        '''
            Load region
        '''
        # Load
        world, region = regionname.split('_')
        regiondata = self.gameserver.getRegion(region)
        #print(regionkwargs)
        globs.currentregion = Region(*regiondata)

        # Create/Clear world sprite groups
        self.worldBlocks = pygame.sprite.Group()
        self.collidableBlocks = pygame.sprite.Group()
        # Special world blocks
        self.climbableBlocks = pygame.sprite.Group()

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

        '''
            Entities
        '''
        # World entities
        self.worldEntitiyBlocks = pygame.sprite.Group()
        self.worldEntities = pygame.sprite.Group()
        # General Entities
        self.players = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()

        self.players.add(globs.character)
        self.entities.add(globs.character)

        self.bouncyBall = BouncyBall(self, (600,600), radius=30)
        self.entities.add(self.bouncyBall)

        self.bouncyBall2 = BouncyBall(self, (1000,630), radius=15)
        self.entities.add(self.bouncyBall2)

        self.zombie = Zombie(self, (2900, 600))
        self.entities.add(self.zombie)

        # Load worldentities
        for worldentity in globs.currentregion.entities:
            self.worldEntities.add(
                worldentity['entity'](self, blockPixel(worldentity['coords'][0], worldentity['coords'][1])))

        # Move character to spawncoords
        print(blockPixel(globs.currentregion.spawnCoordinates[0], globs.currentregion.spawnCoordinates[1]))
        globs.character.move(blockPixel(globs.currentregion.spawnCoordinates[0], globs.currentregion.spawnCoordinates[1]))


        '''
            GUI
        '''
        self.buttons = pygame.sprite.Group()
        self.guiElements = pygame.sprite.Group()

        # ChatBox
        self.chatBox = ChatBox(globs.screen, (5, globs.resolution[1]-35-5-90), (300,90), 5)
        self.guiElements.add(self.chatBox)

        # InputBox
        self.chatInputBox = ChatInputBox(globs.screen, (5, globs.resolution[1]-35), (300,30))
        self.buttons.add(self.chatInputBox)
        self.guiElements.add(self.chatInputBox)


        # Minimap
        self.miniMap = Sprite(globs.screen, (globs.resolution[0]-115,15), (globs.resolution[0]/50, globs.resolution[1]/50))
        self.miniMap.unscaledImage = pygame.surface.Surface((globs.resolution[0]/50, globs.resolution[1]/50))
        self.guiElements.add(self.miniMap)

        # System Menu
        self.systemMenu = SystemMenu(globs.screen)
        #self.guiElements.add(self.systemMenu)


class GameServer():
    def __init__(self, world):
        self.regions = {}
        self.world = world
        #self.region = eval(world + '.' + region + '()')

    def getRegion(self, regionname):
        if not regionname in self.regions:
            self.regions[regionname] = eval(self.world + '.' + regionname + '()')
        return self.regions[regionname].name, self.regions[regionname].spawnCoordinates, self.regions[regionname], self.regions[regionname].entities

def blockPixel(column, row):
    return (column*50-50, row*50-50)