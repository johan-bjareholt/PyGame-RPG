# Libs
import logging
import pygame
import ConfigParser
from importlib import import_module

# Globals
import globals as globs

# The package files
from .cursors import *
from .menu import MainMenu, SettingsMenu

from .ingame import Game
from .worldblocks import *
from .entities import *


logger = logging.getLogger("gfx")

print("Loading graphics")
logger.info("Loading graphics")

# Config parser
config = ConfigParser.ConfigParser()
config.read("settings.conf")

# Location variable
lastLocation = ""

# Clock for fps and events triggered by frames
clock = pygame.time.Clock()

globs.menus = {}
globs.menus['main'] = MainMenu()
globs.menus['settings'] = SettingsMenu()

pygame.display.init()

def loadCursor(name):
    cursor = eval(name)()
    compiledCursor = pygame.cursors.compile(cursor.stringcursor, black=cursor.black, white=cursor.white, xor='o')
    pygame.mouse.set_cursor((8,8),(4,4),*compiledCursor)

def loop():
    mode, sub = globs.location.split('.')
    if mode == "menu":
        menu = globs.menus[sub]
        if lastLocation != globs.location:
            menu.draw()
            global lastLocation
            lastLocation = globs.location
        menu.blitz()
        screen.blit(menu, (0, 0))

    elif mode == "game":
        if lastLocation != globs.location:
            if lastLocation.split('.')[0] != globs.location.split('.')[0]:
                # If first time inGame
                globs.character = Character(screen, (0,0))
                print("Loaded character")
                globs.currentgame = Game(screen)
            globs.currentgame.loadRegion(globs.location.split('.')[1])
        globs.currentgame.loop()

    lastLocation = globs.location
    newFrame()


def newFrame():
    clock.tick(60)
    pygame.display.flip()

def initializeScreen(res=None):
    # Set globs.resolution
    print(res)
    if not res:
        try:
            globs.resolution = config.get("video", "resolution").split('x')
            globs.resolution = map(int, globs.resolution)
            print(globs.resolution)
        except Exception as e:
            print(e)
    else:
        globs.resolution = res
    # Check if fullscreen
    try:
        string = config.get("video", "fullscreen")
        if string == 'True':
            fullscreen = True
        else:
            fullscreen = False
    except Exception as e:
        print(e)
        fullscreen = False

    # Inirialize screen
    global screen
    if fullscreen:
        screen = pygame.display.set_mode(globs.resolution, pygame.FULLSCREEN)
        print("globs.resolution: {}  Fullscreen: {}".format(str(globs.resolution), str(fullscreen)))
    else:
        screen = pygame.display.set_mode(globs.resolution)

globs.initializeScreen = initializeScreen
initializeScreen()
loadCursor("CircleCursor_black")