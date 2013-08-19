import logging
import pygame

import globals as globs

location = globs.location

class Input:
    def __init__(self):
        self.logger = logging.getLogger("input")
        self.logger.info("Loading input")
        print("Loading input")

        self.newly_pressed = {}
        self.events = []
        self.pressed = []

    def loop(self):
        pygame.event.pump()
        ## All events
        self.events = pygame.event.get()
        self.logger.debug(self.events)
        ## Only pressed
        self.pressed = pygame.key.get_pressed()
        #self.logger.debug(self.pressed)
        self.asd()

    def quit(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                return True
        return False

    def asd(self):
        mode, location = globs.location.split('.')
        if mode == "menu":
            for event in self.events:
                if event.type == pygame.MOUSEBUTTONUP:
                    print("Press!")
                    print(event.dict['pos'])
                    print(globs.menus[location])
                    print(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gfx.game.playing = not gfx.game.playing
                if event.type == pygame.MOUSEMOTION:
                    pass