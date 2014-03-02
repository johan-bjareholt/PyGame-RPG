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

    def draw(self):
        # Initialize Singleplayer button
        self.singleplayerButton = Button(self, ((globs.resolution[0]/2)-(200/2), (globs.resolution[1]/2)-100), (200, 50), text="Singleplayer")
        # OnClick action
        def singleplayerButton_clicked(self):
            globs.location = "menu.characters"
        self.singleplayerButton.onClick(singleplayerButton_clicked)
        self.buttons.add(self.singleplayerButton)

        # Initialize Multiplayer button
        self.multiplayerButton = Button(self, ((globs.resolution[0]/2)-(200/2), globs.resolution[1]/2), (200, 50), text="Multiplayer", bgColor=(150,150,150))
        # OnClick action
        def multiplayerButton_clicked(self):
            globs.location = "menu.multiplayerConnectMenu"
        self.multiplayerButton.onClick(multiplayerButton_clicked)
        self.buttons.add(self.multiplayerButton)

        # Initialize Settings button
        self.worldcreatorButton = Button(self, ((globs.resolution[0]/2)-(200/2), (globs.resolution[1]/2)+100), (200, 50), text="Worldcreator", bgColor=(150,150,150))
        def worldcreatorButton_clicked(self):
            pass
        self.worldcreatorButton.onClick(worldcreatorButton_clicked)
        self.buttons.add(self.worldcreatorButton)

        # Initialize Settings button
        self.settingsButton = Button(self, ((globs.resolution[0]/2)-(200/2), (globs.resolution[1]/2)+200), (200, 50), text="Settings")
        def settingsButton_clicked(self):
            globs.location = "menu.settings"
        self.settingsButton.onClick(settingsButton_clicked)
        self.buttons.add(self.settingsButton)

        self.quitButton = QuitButton(self, (25, (globs.resolution[1])-50-25), (100, 50))
        self.buttons.add(self.quitButton)

        # Initialize Title text
        self.titleText = Text((0,0), "My RPG Game", 50)
        self.titleText.rect.topleft = ((globs.resolution[0]/2)-(self.titleText.image.get_width()/2), (globs.resolution[1]/2)-200)

        # Draw title
        self.titleText.draw()

        # Draw buttons
        self.singleplayerButton.draw()
        self.multiplayerButton.draw()
        self.settingsButton.draw()

    def blit(self):
        # Blit all buttons
        self.buttons.draw(globs.screen)
        # Blit title text
        self.titleText.blit()



class CharacterMenu(Menu):
    '''
    The CharacterMenu
    '''
    def __init__(self):
        Menu.__init__(self)

    def draw(self):
        characters = game.characters.listCharacters()
        self.characterContainer = ButtonContainer(self, ((globs.resolution[0]/2)-200-200, (globs.resolution[1]/2)-50), (200,(len(characters)*75)+50), text="Characters")

        if characters:
            self.characterButtons = []
            for i, r in enumerate(characters):
                characterButton = Button(self, (self.characterContainer.rect.topleft[0]+25, self.characterContainer.rect.topleft[1]+45+(75*i)), (150, 50), text=r, bgColor=(200,200,200))
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
                    self.parent.blit()
                self.characterButtons[i].onClick(characterButton_clicked)

                self.buttons.add(self.characterButtons[i])

        self.backButton = BackButton(self, "menu.main", (25, (globs.resolution[1])-50-25), (100, 50))
        self.buttons.add(self.backButton)

        # Initialize Singleplayer button
        self.singleplayerButton = Button(self, ((globs.resolution[0]/2)-100, (globs.resolution[1])-100), (200, 50), text="Start Game", bgColor=(175,175,175))
        # OnClick action
        def singleplayerButton_clicked(self):
            if hasattr(globs, 'charactername'):
                globs.location = "game.world1_StartRegion"
        self.singleplayerButton.onClick(singleplayerButton_clicked)
        self.buttons.add(self.singleplayerButton)

        self.createCharacterButton = Button(self, ((globs.resolution[0]/2)+50, (globs.resolution[1]/2)+50), (200, 50), text="New Character", bgColor=(255,255,255))
        # OnClick action
        def createCharacterButton_clicked(self):
            globs.location = "menu.characterCreator"
        self.createCharacterButton.onClick(createCharacterButton_clicked)
        self.buttons.add(self.createCharacterButton)

        # Initialize Title text
        self.titleText = Text((0,0), "Select your character", 35)
        self.titleText.rect.topleft = ((globs.resolution[0]/2)-(self.titleText.image.get_width()/2), 100)

        # Draw title
        self.titleText.draw()

        # Draw buttons
        self.singleplayerButton.draw()
        #self.settingsButton.draw()

    def blit(self):
        # Blit character container
        self.characterContainer.blit()
        # Blit all buttons
        self.buttons.draw(globs.screen)
        # Blit title text
        self.titleText.blit()


class CreateCharacterMenu(Menu):
    def __init__(self):
        Menu.__init__(self)

    def draw(self):
        # Initialize Title text
        self.titleText = Text((0,0), "Create your character", 35)
        self.titleText.rect.topleft = ((globs.resolution[0]/2)-(self.titleText.image.get_width()/2), 100)

        # Text box
        w = 280
        h = 60
        self.textBox = TextBox(((globs.resolution[0]/2)-(w/2),500), (w,h), 2, alpha=120)
        self.textBox.text = "Name has to be between 5 and 15 characters long"
        self.textBox.draw()

        #Character preview
        wh = (140, 200)
        xy = ((globs.resolution[0]/2)-(wh[0]/2),(globs.resolution[1]/2)-(wh[1]/2))
        self.characterPreview = CharacterPreview(xy, wh)

        # Hair style selector
        hairstyles = ["hair1", "mohawk"]
        x = 800
        y = 200
        self.hairStyleSelector = ListSelector(self, (x,y), (215,50), selectionlist=hairstyles, text="Hairstyle", spacing=2)

        # Hair color selector
        x = 800
        y = 300
        self.hairColorSelector = ColorSelector((x,y), (215,50), text="Haircolor", spacing=2)
        self.hairColorSelector.add_color(self, (220,170,100))
        self.hairColorSelector.add_color(self, (180,120,90))
        self.hairColorSelector.add_color(self, (160,100,80))
        self.hairColorSelector.add_color(self, (120,50,30))
        self.hairColorSelector.add_color(self, (180,50,30))
        self.hairColorSelector.add_color(self, (50,255,50))
        self.hairColorSelector.add_color(self, (50,50,255))

        # Name input box
        x = ((globs.resolution[0]/2)-125)
        y = (globs.resolution[1])-150
        self.nameBox = InputBox((x,y), (250,25), question="Name: ")
        self.nameBox.draw()
        self.buttons.add(self.nameBox)

        # Create character button
        self.createCharacterButton = Button(self, ((globs.resolution[0]/2)-100, (globs.resolution[1])-100), (200, 50), text="New Character", bgColor=(255,255,255))
        def createCharacterButton_clicked(self):
            if len(self.parent.nameBox.inputText)>=5 and len(self.parent.nameBox.inputText)<=15:
                game.characters.create(name=self.parent.nameBox.inputText, 
                                       appearance=self.parent.characterPreview.character.appearance)
                globs.charactername = self.parent.nameBox.inputText
                globs.location = "game.world1_StartRegion"
        self.createCharacterButton.onClick(createCharacterButton_clicked)
        self.buttons.add(self.createCharacterButton)

        # Draw title
        self.titleText.draw()

        self.backButton = BackButton(self, "menu.characters", (25, (globs.resolution[1])-50-25), (100, 50))
        self.buttons.add(self.backButton)

    def blit(self):
        # Blit all buttons
        self.hairStyleSelector.blit()
        self.hairColorSelector.blit()
        self.buttons.draw(globs.screen)
        self.characterPreview.blit()
        # Blit title text
        self.titleText.blit()
        self.textBox.blit()

class SettingsMenu(Menu):
    '''
    The Settings menu

    Used to set the game settings
    '''
    def __init__(self):
        Menu.__init__(self)

    def draw(self):
        # Initialize Title text
        self.settingsText = Text((0,0), "Settings", 50)
        self.settingsText.rect.topleft = ((globs.resolution[0]/2)-(self.settingsText.image.get_width()/2), (globs.resolution[1]/2)-200)

        # Backbutton
        self.backButton = BackButton(self, "menu.main", (25, (globs.resolution[1])-50-25), (100, 50))
        self.buttons.add(self.backButton)

        # Create resolution buttons and container
        resolutions = [(960,540),(1280,720),(1600,900),(1920,1080),(3200,1024)]
        # Container
        self.resolutionContainer = ButtonContainer(self, ((globs.resolution[0]/2)-200-50, (globs.resolution[1]/2)-100), (200,(len(resolutions)*65)+50), text="Display", buttonSpacing=20)
        self.resolutionButtons = []
        # create each button

        for i, r in enumerate(resolutions):
            def resButton_clicked(self):
                globs.resolution = resolutions[self.resolution]
                globs.redraw = True
                globs.initialize_screen()
                globs.config.set("video", "resolution", self.text)
                globs.write_config()
            resButton = self.resolutionContainer.newButton("{}x{}".format(r[0], r[1]), resButton_clicked)
            resButton.resolution = i

        self.versionContainer = Container(self, ((globs.resolution[0]/2)+50, (globs.resolution[1]/2)-100), (300,250), text="Versions")
        self.pythonVersionText = Text((self.versionContainer.rect.topleft[0]+20,self.versionContainer.rect.topleft[1]+50), "Python version: {0[0]}.{0[1]}.{0[2]}".format(sys.version_info), 20)
        self.pygameVersionText = Text((self.versionContainer.rect.topleft[0]+20,self.versionContainer.rect.topleft[1]+80), "PyGame version: {}".format(pygame.version.ver), 20)
        self.sdlVersionText = Text((self.versionContainer.rect.topleft[0]+20,self.versionContainer.rect.topleft[1]+110), "SDL version: {0[0]}.{0[1]}.{0[2]}".format(pygame.get_sdl_version()), 20)
        self.videoDriverText = Text((self.versionContainer.rect.topleft[0]+20,self.versionContainer.rect.topleft[1]+140), "Video driver: {0}".format(pygame.display.get_driver()), 20)
        self.displayInfoText = Text((self.versionContainer.rect.topleft[0]+20,self.versionContainer.rect.topleft[1]+170), "Hardware acceleration: {0}".format(bool(pygame.display.Info().hw)), 20)

        # Fullscreen button
        self.fullscreenButton = ToggleButton(self, (self.versionContainer.rect.topleft[0], self.versionContainer.rect.topleft[1]+self.versionContainer.image.get_height()+20), (230, 50), text="Fullscreen")

        def fullscreenButton_clicked(self):
            globs.fullscreen = not globs.fullscreen
            globs.initialize_screen()
            globs.redraw = True
            globs.config.set("video", "fullscreen", globs.fullscreen)
            globs.write_config()
        self.fullscreenButton.onClick(fullscreenButton_clicked)

        self.buttons.add(self.fullscreenButton)


        # Draw title
        self.settingsText.draw()

    def blit(self):
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
        self.buttons.draw(globs.screen)

        # Blit title text
        self.settingsText.blit()

class MultiplayerConnectMenu(Menu):
    def __init__(self):
        Menu.__init__(self)

    def draw(self):
        self.connectButton = Button(self, ((globs.resolution[0]/2)-100, (globs.resolution[1])-100), (200, 40), text="Connect", bgColor=(255,255,255), fontsize=30)
        # OnClick action
        def connectButton_clicked(self):
            address = self.parent.ipBox.inputText.split(":")[0]
            try:
                port = [self.parent.ipBox.inputText.split(":")[1]]
            except IndexError:
                port = []
            globs.connection = globs.network.ClientConn(address, *port)
            globs.connection.start()
        self.connectButton.clicked = types.MethodType(connectButton_clicked, self.connectButton)
        self.buttons.add(self.connectButton)

        wh = (300, 30)
        xy = (((globs.resolution[0]/2)-(wh[0]/2)),(globs.resolution[1])-150)
        self.ipBox = InputBox(xy, wh, "Address: ")
        self.ipBox.inputText = "127.0.0.1"
        self.ipBox.draw()
        self.buttons.add(self.ipBox)

        # Initialize Title text
        self.titleText = Text((0,0), "Connect", 35)
        self.titleText.rect.topleft = ((globs.resolution[0]/2)-(self.titleText.image.get_width()/2), 100)

        # Draw title
        self.titleText.draw()

        self.backButton = BackButton(self, "menu.main", (25, (globs.resolution[1])-50-25), (100, 50))
        self.buttons.add(self.backButton)

    def blit(self):
        # Blit all buttons
        self.buttons.draw(globs.screen)
        # Blit title text
        self.titleText.blit()
