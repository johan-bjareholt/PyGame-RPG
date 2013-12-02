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
        for entity in self.collidableEntities:
            entity.movement()
        for entity in self.entities:
            entity.events()

        '''
            Background and camera
        '''
        self.blit_background()

        self.updateCamera()

        '''
            World
        '''
        self.update_map_render_size()

        self.blit_world()

        '''
            Entities
        '''

        for entity in self.entities:
            entity.worldBlit()


        '''
            Gui
        '''
        # Update minimap
        self.blitMinimap()

        # Blit add gui elements
        for element in self.guiElements:
            element.blit(globs.screen)

    def update_map_render_size(self):
        self.columnstart = int((globs.cameraX-self.mapalignX)/50)
        self.columnend   = int(self.columnstart+2*(globs.resolution[1]/50))

        self.rowstart = int((globs.cameraY-self.mapalignY)/50)
        self.rowend   = int(self.rowstart+(globs.resolution[0]/50))

    def updateCamera(self):
        # X
        cameraX = globs.character.xy[0]-(globs.resolution[0]/2)
        if not self.smallmapX:
            if cameraX < 0: cameraX = 0
            elif cameraX > globs.currentregion.pixelWidth-globs.resolution[0]: cameraX = globs.currentregion.pixelWidth-(globs.resolution[0])
            self.mapalignX = 0
        else:
            self.mapalignX = globs.character.xy[0]
            cameraX = (globs.currentregion.pixelWidth/2) - (globs.resolution[0]/2)
        # Y
        cameraY = globs.character.xy[1]-(globs.resolution[1]/2)
        if not self.smallmapY:
            if cameraY < 0: cameraY = 0
            elif cameraY > globs.currentregion.pixelHeight-globs.resolution[1]: cameraY = globs.currentregion.pixelHeight-(globs.resolution[1])
            self.mapalignY = 0
        else:
            self.mapalignY = globs.character.xy[1]
            cameraY = (globs.currentregion.pixelHeight/2) - (globs.resolution[1]/2)
        globs.cameraX, globs.cameraY = cameraX, cameraY

    def blit_world(self):
        #if globs.lastCameraX != globs.cameraX or globs.lastCameraY != globs.cameraY:
        rowcount = self.rowstart
        for row in globs.currentregion.renderedmap[self.rowstart:self.rowend]:
            columncount = self.columnstart
            for tile in row[self.columnstart:self.columnend]:
                if tile:
                    tile.worldBlit()
                    #self.screen.blit(tile.image, (tile.xy[0]-globs.cameraX, tile.xy[1]-globs.cameraY))
                    tile.blitDecoration((tile.xy[0]-globs.cameraX, tile.xy[1]-globs.cameraY))
                columncount += 1
            rowcount += 1

    def blitMinimap(self):
        self.miniMap.unscaledImage.fill((0,0,0))
        rowcount = self.rowstart
        for row in globs.currentregion.renderedmap[self.rowstart:self.rowend]:
            columncount = self.columnstart
            for tile in row[self.columnstart:self.columnend]:
                if tile:
                    self.miniMap.unscaledImage.set_at((int((tile.xy[0]-globs.cameraX)/50), int((tile.xy[1]-globs.cameraY)/50)), tile.bgColor)
                columncount += 1
            rowcount += 1
        self.miniMap.image = pygame.transform.scale(self.miniMap.unscaledImage, (100, 100))

    def blit_background(self):
        self.screen.blit(self.backgroundSurface, (0,0))

    def load(self, regionname, spawnCoordinates=None):
        # (Re)load tiles
        self.loadedTiles = {}
        globs.cameraX, globs.cameraY = 0, 0
        globs.lastCameraX, globs.lastCameraY = 0, 0

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

        regiondata = self.gameserver.get_region(region)
        #print(regionkwargs)
        globs.currentregion = Region(*regiondata)

        # Create/Clear world sprite groups
        self.worldBlocks = pygame.sprite.Group()
        self.collidableBlocks = pygame.sprite.Group()
        # Special world blocks
        self.climbableBlocks = pygame.sprite.Group()

        globs.currentregion.renderedmap = []
        # Load blocks
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

        if len(globs.currentregion) < (globs.resolution[0]/50)+1:
            self.smallmapX = len(globs.currentregion)
        else:
            self.smallmapX = False
        if len(globs.currentregion[0]) < (globs.resolution[1]/50)+1:
            self.smallmapY = len(globs.currentregion[0])
        else:
            self.smallmapY = False

        '''
            Entities
        '''
        # World entities
        self.worldEntitiyBlocks = pygame.sprite.Group()
        self.worldEntities = pygame.sprite.Group()
        # General Entities
        self.players = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self.collidableEntities = pygame.sprite.Group()
        self.clickableEntities = pygame.sprite.Group()

        self.players.add(globs.character)
        self.entities.add(globs.character)
        self.collidableEntities.add(globs.character)


        for entity in globs.currentregion.entities:
            xy = blockPixel(entity[1][0], entity[1][1])
            entity[0](globs.screen, xy)
            print(entity)

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

        # Events
        self.eventlist = []

    def pump_events(self):
        for event in eventlist:
            pass

    def get_region(self, regionname):
        if not globs.connection:
            if not regionname in self.regions:
                self.regions[regionname] = eval(self.world + '.' + regionname + '()')
            return self.regions[regionname].name, self.regions[regionname].spawnCoordinates, self.regions[regionname], self.regions[regionname].entities
        else:
            globs.network.game.get_region()
            while not globs.regiondata:
                time.sleep(0.2)
            return globs.regiondata

def blockPixel(column, row):
    return (column*50-50, row*50-50)