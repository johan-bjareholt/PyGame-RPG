import pygame
import os
import sys
import types
import globals as globs


from menu.baseclasses import *
import game


class MainMenu(Menu):
    '''
    The MainMenu

    The first menu shown at startup
    '''
    def __init__(self):
        Menu.__init__(self)

    def drawMain(self):
        # Initialize Singleplayer button
        self.singleplayerButton = Button(self, ((globs.resolution[0]/2)-(200/2), (globs.resolution[1]/2)-100), (200, 50), text="Singleplayer")
        # OnClick action
        def singleplayerButton_clicked(self):
            globs.location = "menu.characters"
        self.singleplayerButton.clicked = types.MethodType(singleplayerButton_clicked, self.singleplayerButton)
        self.buttons.add(self.singleplayerButton)

        # Initialize Multiplayer button
        self.multiplayerButton = Button(self, ((globs.resolution[0]/2)-(200/2), globs.resolution[1]/2), (200, 50), text="Multiplayer", bgColor=(150,150,150))
        # OnClick action
        def multiplayerButton_clicked(self):
            globs.location = "menu.multiplayerConnectMenu"
        self.multiplayerButton.clicked = types.MethodType(multiplayerButton_clicked, self.multiplayerButton)
        self.buttons.add(self.multiplayerButton)

        # Initialize Settings button
        self.worldcreatorButton = Button(self, ((globs.resolution[0]/2)-(200/2), (globs.resolution[1]/2)+100), (200, 50), text="Worldcreator", bgColor=(150,150,150))
        def worldcreatorButton_clicked(self):
            globs.location = "menu.worldcretor"
        self.worldcreatorButton.clicked = types.MethodType(worldcreatorButton_clicked, self.worldcreatorButton)
        self.buttons.add(self.worldcreatorButton)

        # Initialize Settings button
        self.settingsButton = Button(self, ((globs.resolution[0]/2)-(200/2), (globs.resolution[1]/2)+200), (200, 50), text="Settings")
        def settingsButton_clicked(self):
            globs.location = "menu.settings"
        self.settingsButton.clicked = types.MethodType(settingsButton_clicked, self.settingsButton)
        self.buttons.add(self.settingsButton)

        self.quitButton = QuitButton(self, (25, (globs.resolution[1])-50-25), (100, 50))
        self.buttons.add(self.quitButton)

        # Initialize Title text
        self.titleText = Text(self, (0,0), "My RPG Game", 50)
        self.titleText.xy = ((globs.resolution[0]/2)-(self.titleText.image.get_width()/2), (globs.resolution[1]/2)-200)

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



class CharacterMenu(Menu):
    '''
    The CharacterMenu
    '''
    def __init__(self):
        Menu.__init__(self)

    def drawMain(self):
        characters = game.characters.listCharacters()
        self.characterContainer = Container(self, ((globs.resolution[0]/2)-200-200, (globs.resolution[1]/2)-50), (200,(len(characters)*75)+50), text="Characters")
        self.characterButtons = []

        for i, r in enumerate(characters):
            characterButton = Button(self, (self.characterContainer.xy[0]+25, self.characterContainer.xy[1]+45+(75*i)), (150, 50), text=r, bgColor=(200,200,200))
            characterButton.character = r
            self.characterButtons.append(characterButton)

            def characterButton_clicked(self):
                for button in self.parent.characterButtons:
                    button.bgColor=(200,200,200)
                    button.draw()
                self.bgColor = (255,255,255)
                self.draw()
                self.parent.singleplayerButton.draw(bgColor=(255,255,255))
                globs.charactername = self.character
                self.parent.blitz()
            self.characterButtons[i].clicked = types.MethodType(characterButton_clicked, self.characterButtons[i])

            self.buttons.add(self.characterButtons[i])

        self.backButton = BackButton("menu.main", self, (25, (globs.resolution[1])-50-25), (100, 50))
        self.buttons.add(self.backButton)




        # Initialize Singleplayer button
        self.singleplayerButton = Button(self, ((globs.resolution[0]/2)-100, (globs.resolution[1])-100), (200, 50), text="Start Game", bgColor=(175,175,175))
        # OnClick action
        def singleplayerButton_clicked(self):
            if hasattr(globs, 'charactername'):
                globs.location = "game.world1_StartRegion"
        self.singleplayerButton.clicked = types.MethodType(singleplayerButton_clicked, self.singleplayerButton)
        self.buttons.add(self.singleplayerButton)

        self.createCharacterButton = Button(self, ((globs.resolution[0]/2)+50, (globs.resolution[1]/2)+50), (200, 50), text="New Character", bgColor=(255,255,255))
        # OnClick action
        def createCharacterButton_clicked(self):
            globs.location = "menu.characterCreator"
        self.createCharacterButton.clicked = types.MethodType(createCharacterButton_clicked, self.createCharacterButton)
        self.buttons.add(self.createCharacterButton)

        # Initialize Title text
        self.titleText = Text(self, (0,0), "Select your character", 35)
        self.titleText.xy = ((globs.resolution[0]/2)-(self.titleText.image.get_width()/2), 100)

        # Draw title
        self.titleText.draw()

        # Draw buttons
        self.singleplayerButton.draw()
        #self.settingsButton.draw()

    def blitMain(self):
        # Blit character container
        self.characterContainer.blit()
        # Blit all buttons
        self.buttons.draw(self)
        # Blit title text
        self.titleText.blit()


class CreateCharacterMenu(Menu):
    def __init__(self):
        Menu.__init__(self)

    def drawMain(self):
        self.createCharacterButton = Button(self, ((globs.resolution[0]/2)-100, (globs.resolution[1])-100), (200, 50), text="New Character", bgColor=(255,255,255))
        # OnClick action
        def createCharacterButton_clicked(self):
            if len(self.parent.nameBox.inputText)>=5:
                game.characters.create(self.parent.nameBox.inputText)
                globs.charactername = self.parent.nameBox.inputText
                globs.location = "game.world1_StartRegion"
        self.createCharacterButton.clicked = types.MethodType(createCharacterButton_clicked, self.createCharacterButton)
        self.buttons.add(self.createCharacterButton)

        self.nameBox = InputBox(self, (((globs.resolution[0]/2)-125),(globs.resolution[1])-150), (250,25), question="Name: ")
        self.nameBox.draw()
        self.buttons.add(self.nameBox)

        # Initialize Title text
        self.titleText = Text(self, (0,0), "Create your character", 35)
        self.titleText.xy = ((globs.resolution[0]/2)-(self.titleText.image.get_width()/2), 100)

        # Draw title
        self.titleText.draw()

        self.backButton = BackButton("menu.characters", self, (25, (globs.resolution[1])-50-25), (100, 50))
        self.buttons.add(self.backButton)

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
        self.settingsText.xy = ((globs.resolution[0]/2)-(self.settingsText.image.get_width()/2), (globs.resolution[1]/2)-200)

        # Backbutton
        self.backButton = BackButton("menu.main", self, (25, (globs.resolution[1])-50-25), (100, 50))
        self.buttons.add(self.backButton)

        # Create resolution buttons and container
        resolutions = [(960,540),(1280,720),(1600,900),(1920,1080),(3200,1024)]
        # Container
        self.resolutionContainer = Container(self, ((globs.resolution[0]/2)-200-50, (globs.resolution[1]/2)-50), (200,(len(resolutions)*75)+50), text="Display")
        self.resolutionButtons = []
        # create each button
        for i, r in enumerate(resolutions):
            tmpButton = Button(self, (self.resolutionContainer.xy[0]+25, self.resolutionContainer.xy[1]+45+(75*i)), (150, 50), text="{}x{}".format(r[0],r[1]))
            tmpButton.resolution = i
            self.resolutionButtons.append(tmpButton)

            def tmpButton_clicked(self):
                globs.resolution = resolutions[self.resolution]
                globs.redraw = True
                globs.initializeScreen()
            self.resolutionButtons[i].clicked = types.MethodType(tmpButton_clicked, self.resolutionButtons[i])

            self.buttons.add(self.resolutionButtons[i])


        # Fullscreen button
        self.fullscreenButton = Button(self, (self.resolutionContainer.xy[0]+25, self.resolutionContainer.xy[1]+45+(75*i)), (150, 50), text="{}x{}".format(r[0],r[1]))
        self.resolutionButtons.append(tmpButton)

        def fullscreenButton_clicked(self):
            globs.initializeScreen(globs.resolution)
            globs.fullscreen != globs.fullscreen
            globs.redraw = True
        self.fullscreenButton.clicked = types.MethodType(fullscreenButton_clicked, self.fullscreenButton)

        self.buttons.add(self.fullscreenButton)

        self.versionContainer = Container(self, ((globs.resolution[0]/2)+50, (globs.resolution[1]/2)-50), (300,250), text="Versions")
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

class MultiplayerConnectMenu(Menu):
    def __init__(self):
        Menu.__init__(self)

    def drawMain(self):
        self.connectButton = Button(self, ((globs.resolution[0]/2)-100, (globs.resolution[1])-100), (200, 40), text="Connect", bgColor=(255,255,255), fontsize=30)
        # OnClick action
        def connectButton_clicked(self):
            pass
        self.connectButton.clicked = types.MethodType(connectButton_clicked, self.connectButton)
        self.buttons.add(self.connectButton)

        self.ipBox = InputBox(self, (((globs.resolution[0]/2)-125),(globs.resolution[1])-150), (250,40), question="Address: ", fontSize=30)
        self.ipBox.draw()
        self.buttons.add(self.ipBox)

        # Initialize Title text
        self.titleText = Text(self, (0,0), "Connect", 35)
        self.titleText.xy = ((globs.resolution[0]/2)-(self.titleText.image.get_width()/2), 100)

        # Draw title
        self.titleText.draw()

        self.backButton = BackButton("menu.main", self, (25, (globs.resolution[1])-50-25), (100, 50))
        self.buttons.add(self.backButton)

    def blitMain(self):
        # Blit all buttons
        self.buttons.draw(self)
        # Blit title text
        self.titleText.blit()