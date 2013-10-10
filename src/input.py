import logging
import pygame

import globals as globs

location = globs.location

class Input:
    def __init__(self):
        self.logger = logging.getLogger("input")
        self.logger.info("Loading input")
        print("Loading input")

        self.empty_pressed = pygame.key.get_pressed()

        self.events = []

        self.pressed = self.empty_pressed
        self.lastpressed = self.empty_pressed
        self.newly_pressed = self.empty_pressed

    def loop(self):
        self.updateInput()
        self.checkKeys()

    def updateInput(self):
        pygame.event.pump()
        ## All events
        self.events = pygame.event.get()
        self.logger.debug(self.events)
        ## Pressed keys
        self.lastpressed = self.pressed
        self.pressed = pygame.key.get_pressed()
        # New pressed
        self.newly_pressed = [m - n for m,n in zip(self.pressed, self.lastpressed)]
        #self.newly_pressed = self.pressed - self.lastpressed
        #self.logger.debug(self.pressed)

    def checkKeys(self):
        mode, location = globs.location.split('.')
        # General
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if mode == "game":
                        globs.location = "menu.main"
                    elif mode == "menu":
                        globs.running = False
        # Menu
        if mode == "menu":
            for event in self.events:
                if event.type == pygame.MOUSEBUTTONUP:
                    #print(event.dict['pos'])
                    X, Y = event.dict['pos']
                    for button in globs.menus[location].buttons:
                        #print("{} on {}".format(button, ("{}, {}".format(button.X, button.Y))))
                        if button.X <= X and button.X+button.image.W >= X and button.Y <= Y and button.Y+button.image.H >= Y:
                            #print("You pressed da button yeyeyeye!")
                            button.clicked()
                if event.type == pygame.MOUSEMOTION:
                    pass


        # In Game
        elif mode == 'game':
            if self.newly_pressed[pygame.K_e]:
                # entityAction
                globs.character.action()
            if self.newly_pressed[pygame.K_w]:
                # entityAction
                globs.character.worldAction()


            # Movement
            force = 25
            if self.pressed[pygame.K_SPACE]:
                # Up
                globs.character.jump()
            if self.pressed[pygame.K_s]:
                # Down
                pass
            if self.pressed[pygame.K_a]:
                # Left
                globs.character.run("left")
            if self.pressed[pygame.K_d]:
                # Right
                globs.character.run("right")
            if self.pressed[pygame.K_LSHIFT]:
                globs.character.sprint()


    def quit(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                globs.running = False
                return True
        return False