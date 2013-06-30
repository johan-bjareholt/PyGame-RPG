import logging
import pygame


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
        self.logger.debug(self.pressed)

    def quit(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                return True
        return False
