import logging
import os, sys
import time
from importlib import import_module
import pygame
import globals as globs

import cProfile

import input
import graphics
import events

running = True


maindir = os.path.dirname(os.getcwd())

# Logging
logFormat = '%(asctime)-15s %(levelname)s %(name)s:%(lineno)s\t  %(message)s'
logFilename = maindir+"/logs/game/"+time.strftime("%Y-%m-%d %Hh %Mm")+".log"
logging.basicConfig(filename=logFilename, filemode='w', level=logging.DEBUG, format=logFormat)


def load():
    logger = logging.getLogger("main")

    logger.info("Loading game")
    print("Loading game")

    pygame.init()
    globs.clock = pygame.time.Clock()
    globs.inputs = input.Input()
    globs.events = events.Events()
    globs.graphics = graphics


def run():
    globs.running = True
    while globs.running:
        globs.inputs.loop()
        globs.events.loop()
        globs.graphics.loop()
        if globs.inputs.quit():
            globs.running = False
        globs.ticktime = globs.clock.tick(60)
        globs.lastlocation = globs.location

def quit():
    pygame.quit()
    sys.exit()
    #os._quit(0)



if __name__ == '__main__':
    load()
    #inputs.parent = game
    #game.run()
    cProfile.run('run()')
    quit()
