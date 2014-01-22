import pygame
from graphics.baseclasses import Surface, Sprite
from menu.baseclasses import TextBox
from .worlds import *
from .worldblocks import *
from .gui import *
from .entities import BouncyBall, Zombie
from .entities.character import ControlledCharacter
import globals as globs


def load_character():
    globs.character = ControlledCharacter((0,0))


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

        self.update_camera()

        '''
            World
        '''
        self.update_map_render_size()

        self.blit_world()

        '''
            Entities
        '''

        for entity in self.entities.sprites():
            entity.worldBlit()

        '''
            Gui
        '''
        # Update minimap
        self.blit_minimap()

        # Blit add gui elements
        for element in self.guiElements:
            element.blit(globs.screen)

    def update_map_render_size(self):
        if not self.smallmapY:
            self.columnstart = int((globs.cameraX-self.mapalignX)/50)
            self.columnend   = int(self.columnstart+2*(globs.resolution[1]/50))
        else:
            self.columnstart, self.columnend = 0, globs.resolution[1]/50
        if not self.smallmapY:
            self.rowstart = int((globs.cameraY-self.mapalignY)/50)
            self.rowend   = int(self.rowstart+(globs.resolution[0]/50))
        else:
            self.rowstart, self.rowend = 0, globs.resolution[0]/50

    def update_camera(self):
        # X
        cameraX = globs.character.rect.x-(globs.resolution[0]/2)+(globs.character.rect.w/2)
        if not self.smallmapX:
            if cameraX < 0: cameraX = 0
            elif cameraX > globs.currentregion.pixelWidth-globs.resolution[0]: cameraX = globs.currentregion.pixelWidth-(globs.resolution[0])
            self.mapalignX = 0
        else:
            self.mapalignX = globs.character.rect.x
            cameraX = (globs.currentregion.pixelWidth/2) - (globs.resolution[0]/2)
        # Y
        cameraY = globs.character.rect.y-(globs.resolution[1]/2)+(globs.character.rect.h/2)
        if not self.smallmapY:
            if cameraY < 0: cameraY = 0
            elif cameraY > globs.currentregion.pixelHeight-globs.resolution[1]: cameraY = globs.currentregion.pixelHeight-(globs.resolution[1])
            self.mapalignY = 0
        else:
            self.mapalignY = globs.character.rect.y
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
                    tile.blitDecoration((tile.rect.x-globs.cameraX, tile.rect.y-globs.cameraY))
                columncount += 1
            rowcount += 1

    def blit_minimap(self):
        self.miniMap.unscaledImage.fill((0,0,0))
        rowcount = self.rowstart
        for row in globs.currentregion.renderedmap[self.rowstart:self.rowend]:
            columncount = self.columnstart
            for tile in row[self.columnstart:self.columnend]:
                if tile:
                    self.miniMap.unscaledImage.set_at((int((tile.rect.x-globs.cameraX)/50), int((tile.rect.y-globs.cameraY)/50)), tile.bgColor)
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
            Load region
        '''
        # Load
        world, region = regionname.split('_')

        regiondata = self.gameserver.get_region(region)
        globs.currentregion = Region(*regiondata)

        ''' Draw background '''
        background = globs.currentregion.background
        self.backgroundSurface = Surface((globs.resolution[0], globs.resolution[1]))
        self.backgroundSurface.fill(background)

        ''' Set up block groups '''
        self.worldBlocks = pygame.sprite.Group()
        self.collidableBlocks = pygame.sprite.Group()
        # Special world blocks
        self.climbableBlocks = pygame.sprite.Group()

        ''' Load blocks '''
        globs.currentregion.renderedmap = []
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
        ''' See if region is small enough to turn on small region mode '''
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

        ''' Set up entity groups '''
        # World entities
        self.worldEntitiyBlocks = pygame.sprite.Group()
        self.worldEntities = pygame.sprite.Group()
        # General Entities
        self.players = pygame.sprite.Group()
        self.lethals = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.entities = pygame.sprite.LayeredUpdates(default_layer=0)
        self.living_entities = pygame.sprite.Group()
        self.collidableEntities = pygame.sprite.Group()
        self.clickableEntities = pygame.sprite.Group()

        ''' Spawn entities '''
        for entity in globs.currentregion.entities:
            print(entity)
            xy = blockPixel(entity[1][0], entity[1][1])
            entity[0](xy, *entity[2:])

        ''' Spawn character '''
        self.players.add(globs.character)
        self.entities.add(globs.character)
        self.collidableEntities.add(globs.character)
        self.entities.change_layer(globs.character, 8)
        # Move character to spawncoords
        spawn = (blockPixel(globs.currentregion.spawnCoordinates[0], globs.currentregion.spawnCoordinates[1]))
        print(spawn)
        globs.character.rect.move_ip(*spawn)
        print(self.entities.layers())


        '''
            GUI
        '''

        ''' Set up GUI groups '''
        self.buttons = pygame.sprite.Group()
        self.guiElements = pygame.sprite.Group()

        ''' Load GUI elements '''
        # ChatBox
        self.chatBox = ChatBox((5, globs.resolution[1]-35-5-90), (300,90), 5)

        # InputBox
        self.chatInputBox = ChatInputBox((5, globs.resolution[1]-35), (300,30))


        # Minimap
        self.miniMap = Sprite((globs.resolution[0]-115,15), (globs.resolution[0]/50, globs.resolution[1]/50))
        self.miniMap.unscaledImage = pygame.surface.Surface((globs.resolution[0]/50, globs.resolution[1]/50))
        self.guiElements.add(self.miniMap)

        # Username
        xy = (10,10)
        font = globs.getFont("calibrib", 20)
        image = font.render(globs.charactername, True, (0,0,0))
        wh = image.get_size()
        self.username_text = Sprite(xy, wh)
        self.username_text.image.fill((255,0,255))
        self.username_text.image.blit(image, (0,0))
        self.guiElements.add(self.username_text)


        # Healthbar
        xy = (30,10)
        wh = (100,25)
        self.healthbar = ResourceBar(xy, wh, bgColor=(20,20,20), fgColor=(255,0,0))
        self.guiElements.add(self.healthbar)
        self.buttons.add(self.healthbar)

        # Manabar
        xy = (30,40)
        wh = (100,25)
        self.manabar = ResourceBar(xy, wh, bgColor=(20,20,20), fgColor=(0,0,255))
        self.guiElements.add(self.manabar)
        self.buttons.add(self.manabar)

        # Target Healthbar
        xy = (150, 10)
        wh = (100,25)
        self.target_healthbar = ResourceBar(xy, wh, bgColor=(20,20,20), fgColor=(255,0,0))
        self.guiElements.add(self.target_healthbar)

        # Target Manabar
        xy = (150, 40)
        wh = (100,25)
        self.target_healthbar = ResourceBar(xy, wh, bgColor=(20,20,20), fgColor=(0,0,255))
        self.guiElements.add(self.target_healthbar)

        # System Menu
        self.systemMenu = SystemMenu(self)


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
            return self.regions[regionname].name, self.regions[regionname].spawnCoordinates, self.regions[regionname], self.regions[regionname].entities, self.regions[regionname].background
        else:
            globs.network.game.get_region()
            while not globs.regiondata:
                time.sleep(0.2)
            return globs.regiondata

def blockPixel(column, row):
    return (column*50-50, row*50-50)