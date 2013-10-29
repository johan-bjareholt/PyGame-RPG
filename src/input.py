import logging
import pygame

import main
import globals as globs
import graphics

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
        self.textBoxRefreshCheck()
        self.checkKeys()

    def textBoxRefreshCheck(self):
        if globs.location != globs.lastlocation:
            globs.focused = None

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
        if mode == "menu":
            location = globs.menus[location]
        elif mode == "game":
            location = globs.currentgame

        # General
        if self.keydown(pygame.K_ESCAPE):
            if globs.focused:
                globs.focused.unfocus()
            else:
                if mode == "game":
                    globs.location = "menu.main"
                elif mode == "menu" and location.__class__.__name__ != "MainMenu":
                    location.backButton.clicked()
                elif mode == "menu":
                    globs.running = False
        if self.keydown(pygame.K_F12):
            graphics.screenshot()

        for event in self.events:
            if event.type == pygame.MOUSEBUTTONUP:
                #print(event.dict['pos'])
                X, Y = event.dict['pos']
                for button in location.buttons:
                    #print("{} on {}".format(button, ("{}, {}".format(button.X, button.Y))))
                    if button.X <= X and button.X+button.image.W >= X and button.Y <= Y and button.Y+button.image.H >= Y:
                        #print("You pressed da button yeyeyeye!")
                        button.clicked()
            if event.type == pygame.MOUSEMOTION:
                pass

        # If something is focused
        if globs.focused:
            #print(globs.focused.__class__.__name__)
            # If a textbox is focused
            if globs.focused.__class__.__name__ in ['InputBox', 'ChatInputBox']:
                self.textBoxInput()

        # In Game
        elif mode == 'game':
            if self.newly_pressed[pygame.K_e]:
                # entityAction
                globs.character.action()
            if self.newly_pressed[pygame.K_w]:
                # entityAction
                globs.character.worldAction()

            if self.newly_pressed[pygame.K_RETURN]:
                globs.currentgame.chatInputBox.clicked()


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

    def textBoxInput(self):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                inkey = event.key
                if inkey == pygame.K_BACKSPACE:
                    globs.focused.inputText = globs.focused.inputText[0:-1]
                    globs.focused.draw()
                elif inkey == pygame.K_RETURN:
                    globs.focused.unfocus()
                elif inkey <= 127:
                    if self.pressed[pygame.K_LSHIFT] or self.pressed[pygame.K_RSHIFT]:
                        globs.focused.inputText += chr(inkey).capitalize()
                    else:
                        globs.focused.inputText += chr(inkey) 
                    globs.focused.draw()

    def keydown(self, key):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == key:
                    return True
        return False

    def keyup(self, key):
        for event in self.events:
            if event.type == pygame.KEYUP:
                if event.key == key:
                    return True
        return False

    def quit(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                return True
        return False