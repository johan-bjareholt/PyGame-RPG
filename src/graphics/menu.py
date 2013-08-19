import pygame
import os
import types

import globals as globs

resolution = globs.resolution

from .baseclasses import Surface, Button, Text


class Menu(Surface):
    '''
    Base class for the menus
    '''
    def __init__(self, bgImage="/sky.jpg", bgColor=(0, 0, 0), font="calibri"):
        Surface.__init__(self, resolution)

        self.background = self.subsurface((0, 0), resolution)
        self.main = self.subsurface((0, 0), resolution)
        self.foreground = self.subsurface((0, 0), resolution)

        self.buttons = pygame.sprite.Group()

        # Background initialization
        if bgImage:
            self.backgroundImage = pygame.image.load(os.getcwd()+bgImage)
            self.backgroundImage = pygame.transform.scale(self.backgroundImage, resolution)
        self.backgroundColor = bgColor

        self.fontname = font


    #
    # Background layer
    #
    def drawBackground(self):
        if self.backgroundImage:
            self.background.blit(self.backgroundImage, (0, 0))
        else:
            self.background.fill(self.backgroundColor)

    def blitBackground(self):
        pass

    #
    # Main layer
    #
    def drawMain(self):
        pass

    def blitMain(self):
        pass

    #
    # Foreground layer
    #
    def drawForeground(self):
        pass

    def blitForeground(self):
        pass

    #
    # Main commands
    #
    def draw(self):
        self.drawBackground()
        self.drawMain()
        self.drawForeground()

    def blitz(self):
        self.blitBackground()
        self.blitMain()
        self.blitForeground()



'''
The complete menus are down here!
'''



class MainMenu(Menu):
    '''
    The MainMenu

    The first menu shown at startup
    '''
    def __init__(self):
        Menu.__init__(self)

    def drawMain(self):
        #class Button1(Button):
        #    def __init__(self):
        #        Button.__init__(self, globs.menus['main'], ((resolution[0]/2)-(100/2), (resolution[1]/2)-100), (100, 25), text="Hello")
        self.button1 = Button(self, ((resolution[0]/2)-(100/2), (resolution[1]/2)-100), (100, 25), text="Hello")
        #self.button1 = Button1()
        def button1_clicked(self):
            print("You clicked button1!")
        #self.button1.clicked = button1_clicked
        self.button1.clicked = types.MethodType(button1_clicked, self.button1)
        self.buttons.add(self.button1)

        print(self.button1.clicked)
        self.button1.clicked()

        self.button2 = Button(self, ((resolution[0]/2)-(100/2), resolution[1]/2), (100, 25), text="Hello2")
        self.buttons.add(self.button2)

        self.button3 = Button(self, ((resolution[0]/2)-(100/2), (resolution[1]/2)+100), (100, 25), text="Hello3")
        self.buttons.add(self.button3)

        # Title text
        self.titleText = Text(self, (0,0), "My RPG Game", 50)
        self.titleText.xy = ((resolution[0]/2)-(self.titleText.image.get_width()/2), (resolution[1]/2)-200)

        self.button1.draw()
        self.button2.draw()
        self.button3.draw()

        self.titleText.draw()

    def blitMain(self):
        self.buttons.draw(self)
        self.titleText.blit()