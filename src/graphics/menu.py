import pygame
import os
import sys
import types

import globals as globs

resolution = globs.resolution

from .baseclasses import Surface, Button, QuitButton, BackButton, Container, Text


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
        # Initialize Singleplayer button
        self.singleplayerButton = Button(self, ((resolution[0]/2)-(200/2), (resolution[1]/2)-100), (200, 50), text="Singleplayer")
        # OnClick action
        def singleplayerButton_clicked(self):
            globs.location = "game.world1_StartRegion"
        self.singleplayerButton.clicked = types.MethodType(singleplayerButton_clicked, self.singleplayerButton)
        self.buttons.add(self.singleplayerButton)

        # Initialize Multiplayer button
        self.multiplayerButton = Button(self, ((resolution[0]/2)-(200/2), resolution[1]/2), (200, 50), text="Multiplayer(WIP)")
        # OnClick action
        def multiplayerButton_clicked(self):
            print("You clicked multiplayerButton!")
        self.multiplayerButton.clicked = types.MethodType(multiplayerButton_clicked, self.multiplayerButton)
        self.buttons.add(self.multiplayerButton)

        # Initialize Settings button
        self.worldcreatorButton = Button(self, ((resolution[0]/2)-(200/2), (resolution[1]/2)+100), (200, 50), text="Worldcreator(WIP)")
        def worldcreatorButton_clicked(self):
            globs.location = "menu.worldcretor"
        self.worldcreatorButton.clicked = types.MethodType(worldcreatorButton_clicked, self.worldcreatorButton)
        self.buttons.add(self.worldcreatorButton)

        # Initialize Settings button
        self.settingsButton = Button(self, ((resolution[0]/2)-(200/2), (resolution[1]/2)+200), (200, 50), text="Settings")
        def settingsButton_clicked(self):
            globs.location = "menu.settings"
        self.settingsButton.clicked = types.MethodType(settingsButton_clicked, self.settingsButton)
        self.buttons.add(self.settingsButton)

        self.quitButton = QuitButton(self, (25, (resolution[1])-50-25), (100, 50))
        self.buttons.add(self.quitButton)

        # Initialize Title text
        self.titleText = Text(self, (0,0), "My RPG Game", 50)
        self.titleText.xy = ((resolution[0]/2)-(self.titleText.image.get_width()/2), (resolution[1]/2)-200)

        # Draw title
        self.titleText.draw()

        # Draw buttons
        self.singleplayerButton.draw()
        self.multiplayerButton.draw()
        self.settingsButton.draw()

    def blitMain(self):
        # Blit all buttons
        self.buttons.draw(self)
        # Blit title text
        self.titleText.blit()

class SettingsMenu(Menu):
    '''
    The Settings menu

    Used to set the game settings
    '''
    def __init__(self):
        Menu.__init__(self)

    def drawMain(self):
        # Initialize Title text
        self.settingsText = Text(self, (0,0), "Settings", 50)
        self.settingsText.xy = ((resolution[0]/2)-(self.settingsText.image.get_width()/2), (resolution[1]/2)-200)

        # Backbutton
        self.backButton = BackButton("menu.main", self, (25, (resolution[1])-50-25), (100, 50))
        self.buttons.add(self.backButton)

        # Create resolution buttons and container
        resolutions = [(960,540),(1280,720),(1600,900),(1920,1080)]
        # Container
        self.resolutionContainer = Container(self, ((resolution[0]/2)-200-50, (resolution[1]/2)-50), (200,(len(resolutions)*75)+50), text="Display")
        self.resolutionButtons = []
        # create for each button
        for res in range(len(resolutions)):
            tmpButton = Button(self, (self.resolutionContainer.xy[0]+25, self.resolutionContainer.xy[1]+45+(75*res)), (150, 50), text="{}x{}".format(resolutions[res][0],resolutions[res][1]))
            self.resolutionButtons.append(tmpButton)

            def tmpButton_clicked(self):
                globs.initializeScreen((resolutions[res][0], resolutions[res][1]))
            self.resolutionButtons[res].clicked = types.MethodType(tmpButton_clicked, self.resolutionButtons[res])

            self.buttons.add(self.resolutionButtons[res])

        self.versionContainer = Container(self, ((resolution[0]/2)+50, (resolution[1]/2)-50), (300,250), text="Versions")
        self.pythonVersionText = Text(self, (self.versionContainer.xy[0]+20,self.versionContainer.xy[1]+50), "Python version: {0[0]}.{0[1]}.{0[2]}".format(sys.version_info), 20)
        self.pygameVersionText = Text(self, (self.versionContainer.xy[0]+20,self.versionContainer.xy[1]+80), "PyGame version: {}".format(pygame.version.ver), 20)
        self.sdlVersionText = Text(self, (self.versionContainer.xy[0]+20,self.versionContainer.xy[1]+110), "SDL version: {0[0]}.{0[1]}.{0[2]}".format(pygame.get_sdl_version()), 20)
        self.videoDriverText = Text(self, (self.versionContainer.xy[0]+20,self.versionContainer.xy[1]+140), "Video driver: {0}".format(pygame.display.get_driver()), 20)
        self.displayInfoText = Text(self, (self.versionContainer.xy[0]+20,self.versionContainer.xy[1]+170), "Hardware acceleration: {0}".format(bool(pygame.display.Info().hw)), 20)

        # Draw title
        self.settingsText.draw()

    def blitMain(self):
        # Blit resolutionContainer
        self.resolutionContainer.blit()

        # Blit versionContainer
        self.versionContainer.blit()
        self.pythonVersionText.blit()
        self.pygameVersionText.blit()
        self.sdlVersionText.blit()
        self.videoDriverText.blit()
        self.displayInfoText.blit()

        # Blit all buttons
        self.buttons.draw(self)

        # Blit title text
        self.settingsText.blit()