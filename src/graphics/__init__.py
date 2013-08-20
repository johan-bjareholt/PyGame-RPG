# Libs
import logging
import pygame
import ConfigParser

# Globals
import globals as globs

# The package files
from .cursors import *
from .menu import MainMenu, SettingsMenu
from .world import World


logger = logging.getLogger("gfx")

print("Loading graphics")
logger.info("Loading graphics")

# Config parser
config = ConfigParser.ConfigParser()
config.read("settings.conf")

# Location variable
drawnLocation = ""

# Clock for fps and events triggered by frames
clock = pygame.time.Clock()

globs.menus = {}
globs.menus['main'] = MainMenu()
globs.menus['settings'] = SettingsMenu()

def loadCursor(name):
    cursor = eval(name)()
    compiledCursor = pygame.cursors.compile(cursor.stringcursor, black=cursor.black, white=cursor.white, xor='o')
    pygame.mouse.set_cursor((8,8),(4,4),*compiledCursor)

def loop():
    mode, sub = globs.location.split('.')
    if mode == "menu":
        menu = globs.menus[sub]
        if drawnLocation != globs.location:
            screen.fill((255,255,255))
            menu.draw()
            global drawnLocation
            drawnLocation = globs.location
        menu.blitz()
        screen.blit(menu, (0, 0))

    elif mode == "game":
        pass

    newFrame()


def newFrame():
    clock.tick(60)
    pygame.display.flip()

def initializeScreen():
    # Set resolution
    global resolution
    try:
        resolution = config.get("video", "resolution").split('x')
        resolution = map(int, resolution)
        print(resolution)
    except Exception as e:
        print(e)
    globs.resolution = resolution
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
        screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
        print("Resolution: {}  Fullscreen: {}".format(str(resolution), str(fullscreen)))
    else:
        screen = pygame.display.set_mode(resolution)
    globs.screen = screen

initializeScreen()
loadCursor("CircleCursor_black")