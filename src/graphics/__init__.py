# Libs
import logging
import pygame
import datetime
from importlib import import_module

# Globals
import globals as globs

# The package files
from .cursors import *
from menu import *

from game import GameClient
from game.worldblocks import *
from game.entities import *
from .baseclasses import Text


logger = logging.getLogger("gfx")

print("Loading graphics")
logger.info("Loading graphics")

# Clock for fps and events triggered by frames

pygame.display.init()

# Draw queue
globs.drawqueue = []


def loadMenus():
    globs.menus = {}
    globs.menus['main'] = MainMenu()
    globs.menus['settings'] = SettingsMenu()
    globs.menus['characters'] = CharacterMenu()
    globs.menus['characterCreator'] = CreateCharacterMenu()
    globs.menus['multiplayerConnectMenu'] = MultiplayerConnectMenu()

def loop():
    mode, sub = globs.location.split('.')
    if mode == "menu":
        if globs.lastlocation != globs.location or globs.redraw:
            globs.menus[sub].draw()
            globs.redraw = False
        globs.menus[sub].blitz()
        screen.blit(globs.menus[sub], (0, 0))

    elif mode == "game":
        if globs.lastlocation != globs.location:
            if globs.lastlocation.split('.')[0] != globs.location.split('.')[0]:
                # If first time inGame
                globs.character = Character(screen, (0,0))
                #print("Loaded character")
                globs.currentgame = GameClient(screen)
            globs.currentgame.loadRegion(sub)
        globs.currentgame.loop()

    fpsCounter()

    pygame.display.flip()


def fpsCounter():
    globs.fpstext = Text(screen, (0,0), str(globs.clock.get_fps())[:2], 30, color=(150,150,150))
    globs.fpstext.blit()

def initializeScreen():
    # Set globs.resolution
    if hasattr(globs, "resolution"):
        pass
    else:
        string = globs.config.get("video", "resolution")
        globs.resolution = globs.config.get("video", "resolution").split('x')
        globs.resolution = map(int, globs.resolution)

    # Check if fullscreen
    if hasattr(globs, "fullscreen"):
        fullscreen = globs.fullscreen
    else:
        string = globs.config.get("video", "fullscreen")
        if string == 'True':
            fullscreen = True
        else:
            fullscreen = False
        globs.fullscreen = fullscreen
    # Inirialize screen
    global screen
    if fullscreen:
        screen = pygame.display.set_mode(globs.resolution, pygame.FULLSCREEN)
        print("Resolution: {}  Fullscreen: {}".format(str(globs.resolution), str(fullscreen)))
    else:
        screen = pygame.display.set_mode(globs.resolution)
    globs.screen = screen

    # Reinitialize menus for new resolution
    loadMenus()

def screenshot():
    pygame.image.save(globs.screen, "test.png")

def loadCursor(name):
    cursor = eval(name)()
    compiledCursor = pygame.cursors.compile(cursor.stringcursor, black=cursor.black, white=cursor.white, xor='o')
    pygame.mouse.set_cursor((8,8),(4,4),*compiledCursor)

globs.initializeScreen = initializeScreen
initializeScreen()
loadCursor("CircleCursor_black")