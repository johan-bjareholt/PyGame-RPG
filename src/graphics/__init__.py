# Libs
import logging
import pygame

# The package files
from .menu import MainMenu, Button
from .world import World

logger = logging.getLogger("gfx")

print("Loading graphics")
logger.info("Loading graphics")

location = "menu.main"
drawnLocation = ""


global X, Y
X, Y = 1280, 720
global screen

fullscreen = False
if fullscreen:
    screen = pygame.display.set_mode((X, Y), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((X, Y))


clock = pygame.time.Clock()


stuffToBlit = []


def loop():
    if drawnLocation != location:
        draw()
    blit()
    newFrame()


def newFrame():
    clock.tick(60)
    pygame.display.flip()


def draw():
    menu = MainMenu()
    button1 = Button((25, 25), (25, 25))
    stuffToBlit.append(menu)
    stuffToBlit.append(button1)

def blit():
    mode = location.split('.')[0]
    if mode == 'menu':
        for stuff in stuffToBlit:
            screen.blit(stuff, stuff.XY)
    elif mode == 'game':
        pass
