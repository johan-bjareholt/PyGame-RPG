# Libs
import logging
import pygame

# Globals
import globals as globs

# The package files
from .cursors import *
from .menu import MainMenu
from .world import World


logger = logging.getLogger("gfx")

print("Loading graphics")
logger.info("Loading graphics")


# Initialize variables
resolution = globs.resolution
location = globs.location
drawnLocation = ""

fullscreen = False
if fullscreen:
    screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(resolution)

clock = pygame.time.Clock()

globs.menus = {}
globs.menus['main'] = MainMenu()

def loadCursor(name):
    cursor = eval(name)()
    compiledCursor = pygame.cursors.compile(cursor.stringcursor, black=cursor.black, white=cursor.white, xor='o')
    pygame.mouse.set_cursor((8,8),(4,4),*compiledCursor)

def loop():
    mode, sub = location.split('.')
    if mode == "menu":
        menu = globs.menus[sub]
        if drawnLocation != location:
            menu.draw()
            global drawnLocation
            drawnLocation = location
        menu.blitz()
        screen.blit(menu, (0, 0))

    elif mode == "game":
        pass

    newFrame()


def newFrame():
    clock.tick(60)
    pygame.display.flip()

loadCursor("CircleCursor_black")