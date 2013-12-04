import logging
import string
import pygame

import main
import globals as globs
import graphics

location = globs.location

shiftsymbols = {
    '1':'!',
    '2':'"',
    '3':'#',
    '4':'$',
    '5':'%',
    '6':'&',
    '7':'/',
    '8':'(',
    '9':')',
    '0':'=',
    '+':'?',

    '.':':',
    ',':';',
}
altsymbols = {
    '1':'!',
    '2':'@',
    '3':'#',
    '4':'$',
    '5':'%',
    '6':'&',
    '7':'{',
    '8':'[',
    '9':']',
    '0':'}',
    '+':'\\',
}

class Input:
    def __init__(self):
        self.logger = logging.getLogger("input")
        self.logger.info("Loading input")

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
        #self.logger.debug(self.events)
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

        # What escape does in different locations
        if self.keydown(pygame.K_ESCAPE):
            if globs.focused:
                globs.focused.unfocus()
            else:
                if mode == "game":
                    globs.currentgame.systemMenu.toggle()
                elif mode == "menu" and location.__class__.__name__ != "MainMenu":
                    location.backButton.clicked()
                elif mode == "menu":
                    globs.running = False
        # Screenshot
        if self.keydown(pygame.K_F12):
            graphics.screenshot()

        for event in self.events:
            if event.type == pygame.MOUSEBUTTONUP:
                #print(event.dict['pos'])
                X, Y = event.dict['pos']
                if mode == "menu":
                    buttonlist = location.buttons
                elif mode == "game":
                    if globs.focused:
                        buttonlist = location.buttons
                    else:
                        buttonlist = globs.currentgame.clickableEntities

                for button in buttonlist:
                    #print("{} on {}".format(button, ("{}, {}".format(button.X, button.Y))))
                    if button.rect.collidepoint(X, Y):
                    #if button.X <= X and button.X+button.image.get_width() >= X and button.Y <= Y and button.Y+button.image.get_height() >= Y:
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
                pass
                #globs.character.action()
            if self.newly_pressed[pygame.K_w]:
                # entityAction
                globs.character.worldAction()

            if self.newly_pressed[pygame.K_RETURN]:
                if self.keydown(pygame.K_RETURN):
                    globs.currentgame.chatInputBox.clicked()

            if pygame.mouse.get_pressed()[0]:
                globs.character.weapon.attack()


            # Movement
            force = 25
            if self.pressed[pygame.K_SPACE]:
                # Jump
                globs.character.jump()
            if self.pressed[pygame.K_w]:
                # Up (Climb)
                globs.character.climb()
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
                    character = ""
                    if self.pressed[pygame.K_LSHIFT] or self.pressed[pygame.K_RSHIFT]:
                        if chr(inkey) in string.ascii_lowercase:
                            character = chr(inkey).capitalize()
                        else:
                            try:
                                character = shiftsymbols[chr(inkey)]
                            except KeyError:
                                character = chr(inkey)
                    elif self.pressed[pygame.K_RALT] or self.pressed[pygame.K_LALT]:
                        if chr(inkey) in string.ascii_lowercase:
                            character = chr(inkey).capitalize()
                        else:
                            try:
                                character = altsymbols[chr(inkey)]
                            except KeyError:
                                character = chr(inkey)
                    else:
                        character = chr(inkey) 
                    globs.focused.inputText += character
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