from graphics.baseclasses import *
import types
from importlib import import_module


class Menu:
    '''
    Base class for the menus
    '''
    def __init__(self, bgImage="/menubackground.jpg", bgColor=(0, 0, 0), font="calibri"):
        self.background = Surface(globs.resolution)
        self.buttons = pygame.sprite.Group()

        # Background initialization
        if bgImage:
            self.backgroundImage = pygame.image.load(globs.datadir+bgImage)
            self.backgroundImage = pygame.transform.scale(self.backgroundImage, globs.resolution)
        self.backgroundColor = bgColor

        self.fontname = font

        self.drawBackground()

    # Background
    def drawBackground(self):
        if self.backgroundImage:
            globs.screen.blit(self.backgroundImage, (0, 0))
        else:
            globs.screen.fill(self.backgroundColor)

    def blitMain(self):
        pass

    # Main commands
    def draw(self):
        pass

    def blit(self):
        pass


class Container(Sprite):
    def __init__(self, parent, xy, wh, bgColor=(235,235,235), text='', textsize=10, spacing=2):
        Sprite.__init__(self, xy, wh)
        self.text = text
        self.bgColor = bgColor
        self.spacing = spacing
        self.entries = []

    def draw(self):
        self.image.fill((255,255,255))
        x = 10
        y = self.spacing

        # Draw text
        self.textSprite = Text(self, x+self.rect.x, y+self.rect.x, self.textsize)
        x += self.textsize + self.spacing

        # Draw entries
        for entry in self.entries:
            entry.localxy = (y, x)
            entry.rect.topleft = (x+self.rect.x, y+self.rect.y)
            x += entry.rect.x + self.spacing

    def addEntry(self, sprite, w=None, h=None):
        if not w:
            w = self.image.get_width()-(self.buttonSpacing*2)
        if not h:
            h = 35

        self.entries.append(sprite)



class ButtonContainer(Sprite):
    def __init__(self, parent, xy, wh, bgColor=(235,235,255), text='',
                 buttonBgColor=(255,255,255), buttonFgColor=(0,0,0), buttonH=50, buttonSpacing=10):
        Sprite.__init__(self, xy, wh)
        self.parent = parent
        self.image.fill(bgColor)
        self.text = text

        self.buttons = []
        self.buttonH = buttonH
        self.buttonSpacing = buttonSpacing
        self.buttonBgColor = buttonBgColor
        self.buttonFgColor = buttonFgColor

        self.drawText()
        self.updateButtons()

    def drawText(self):
        self.textSprite = Text((10,10), self.text, 25)
        self.image.blit(self.textSprite.image, self.textSprite.rect.topleft)

    def updateButtons(self):
        for button in range(len(self.buttons)):
            self.buttons[button].localxy = (self.buttonSpacing, 
                                           ((self.textSprite.image.get_height()+self.textSprite.rect.topleft[1])+
                                           (self.buttonSpacing*button)+(self.buttonH*button)))

            self.buttons[button].rect.topleft = ((self.buttons[button].localxy[0]+self.rect.topleft[0] ,
                                              self.buttons[button].localxy[1]+self.rect.topleft[1]))

    def newButton(self, text, function):
        # Set variables
        xy=(50,50)
        wh=(self.image.get_width()-(self.buttonSpacing*2),
            self.buttonH)

        # Initialize button
        newbutton = Button(self.parent, xy, wh, bgColor=self.buttonBgColor, fgColor=self.buttonFgColor, text=text)
        newbutton.onClick(function)

        # Add button to container and return it
        self.buttons.append(newbutton)
        self.updateButtons()
        #print(newbutton.xy)
        if globs.location.split('.')[0] == "menu":
            globs.menus[globs.location.split('.')[1]].buttons.add(newbutton)
        else:
            globs.currentgame.buttons.add(newbutton)
        return newbutton

class Button(Sprite):
    def __init__(self, parent, xy, wh, bgColor=(255, 255, 255), fgColor=(0, 0, 0), text=None, font="calibri", fontsize=None, textColor=(0, 0, 0), borderRadius=5):
        Sprite.__init__(self, xy, wh)
        self.parent = parent

        self.bgColor = bgColor
        self.fgColor = fgColor
        self.textColor = textColor
        self.text = text
        self.fontname = font
        self.fontsize = fontsize
        self.borderRadius = borderRadius
        self.draw()

    def draw(self, bgColor=None):
        # Fill background
        if not bgColor:
            self.image.fill(self.bgColor)
        else:
            self.image.fill(bgColor)
        if self.borderRadius:
            self.cutBorderRadius(self.borderRadius)
        # Apply text
        if self.text:
            self.drawText()

    def drawText(self):
        # Adapt fontsize
        if not self.fontsize:
            self.fontsize = (self.image.get_height()/2)+2
        # Load font
        self.font = globs.getFont(self.fontname, self.fontsize)
        self.renderedText = self.font.render(self.text, True, self.textColor)
        # Center text
        x = (self.image.get_width()-self.renderedText.get_width())/2
        y = (self.image.get_height()-self.fontsize)/2
        # Blit to sprites surface
        self.image.blit(self.renderedText, (x, y))

    def onClick(self, function):
        self.clicked = types.MethodType(function, self)

    def clicked(self):
        print("You just clicked me!")

class ToggleButton(Button):
    def __init__(self, parent, xy, wh, default=False, bgColor=(255, 255, 255), fgColor=(0, 0, 0), text=None, font="calibri", fontsize=None):
        self.state = globs.fullscreen
        Button.__init__(self, parent, xy, wh, bgColor, fgColor, text, font, fontsize)

    def draw(self, bgColor=None):
        # Fill background
        if not bgColor:
            self.image.fill(self.bgColor)
        else:
            self.image.fill(bgColor)
        # Apply text
        if self.text:
            # Adapt fontsize
            if not self.fontsize:
                self.fontsize = (self.image.get_height()/2)+2
            # Load font
            self.font = globs.getFont(self.fontname, self.fontsize)
            self.renderedText = self.font.render(self.text, True, pygame.color.Color(0, 0, 0))
            # Center text
            x = self.image.get_height()/4
            y = (self.image.get_height()-self.fontsize)/2
            # Blit to sprites surface
            self.image.blit(self.renderedText, (x, y))
        # Apply toggle thingy
        h = self.image.get_height()*3/4
        w = int(h*2)
        toggleImage = pygame.surface.Surface((w, h))
        if self.state == True:
            statetext = "On"
            toggleImage.fill((30,200,30))
        elif self.state == False:
            statetext = "Off"
            toggleImage.fill((200,30,30))
        x = self.image.get_width()-w-10
        y = (self.image.get_height()-h)/2
        self.image.blit(toggleImage, (x, y))


    def clicked(self):
        self.state != self.state
        self.draw()

class TextBox(Sprite):
    def __init__(self, xy, wh, rows, spacing=3, font='calibri', fgColor=(0, 0, 0), bgColor=(255, 255, 255), alpha=None, reverse=False):
        Sprite.__init__(self, xy, wh)
        self.font = font
        self.bgColor = bgColor
        self.fgColor = fgColor
        self.alpha = alpha
        self.text = ""
        self.focus = False
        self.rows = rows
        self.spacing = spacing
        self.reverse = reverse

        self.loadFont()
        self.draw()

    def draw(self):
        self.image.fill(self.bgColor)
        if self.alpha:
            self.image.set_alpha(self.alpha)
        self.drawFrame()
        self.drawText()

    def loadFont(self):
        '''
            It is recommended to use monospace fonts in the TextBox
        '''
        totalspacing = self.spacing*self.rows+self.spacing
        self.fontSize = ((self.image.get_height()-totalspacing)/self.rows)-self.spacing
        #self.fontSize = self.image.get_height()-4
        self.font = globs.getFont(self.font, self.fontSize)

    def drawText(self):
        charcount = self.text.count('')
        charwidth = self.font.size('a')[0]
        chars_per_row = (self.image.get_width()/charwidth)

        entries = self.text.split('\n')
        if self.reverse:
            entries = reversed(entries)
        entrynum = len(self.text.split('\n'))
        if self.reverse:
            rownum = self.rows-1
        else:
            rownum = 0
        for entry in entries:
            if self.reverse:entrynum -= 1
            else: entrynum += 1
            for row in range((len(entry)/chars_per_row)+1):
                text = entry[row*chars_per_row:(row+1)*chars_per_row]
                if text:
                    print(text)
                    rendered_text = self.font.render(text, True, pygame.color.Color(self.fgColor[0], self.fgColor[1], self.fgColor[2]))
                    self.image.blit(rendered_text, (self.spacing, self.spacing+(rownum*self.spacing)+(rownum*self.fontSize)))
                    if self.reverse:
                        rownum -= 1
                    else:
                        rownum += 1

    def drawFrame(self):
        pass

class InputBox(Sprite):
    def __init__(self, xy, wh, question="", fgColor=(0, 0, 0), bgColor=(255, 255, 255), alpha=None, font='droidsansmono', fontSize=None, spacing=2):
        Sprite.__init__(self, xy, wh)
        self.bgColor = bgColor
        self.fgColor = fgColor
        self.alpha = alpha
        self.font = font
        self.spacing = spacing
        self.question = question
        self.inputText = ""
        self.fontSize = fontSize
        self.focus = False
        self.loadFont()
        self.draw()

    def draw(self):
        self.image.fill(self.bgColor)
        if self.alpha:
            self.image.set_alpha(self.alpha)
        self.drawFrame()
        self.drawText()

    def loadFont(self):
        if not self.fontSize:
            self.fontSize = self.image.get_height()-(self.spacing*2)
        self.font = globs.getFont(self.font, self.fontSize)

    def drawText(self):
        text = self.question + self.inputText
        maxchars = self.image.get_width()/self.font.size("a")[0]
        startchar = len(text)-maxchars
        if startchar < 0: 
            startchar = 0
        text = text[startchar:]
        rendered_text = self.font.render(text, True, pygame.color.Color(self.fgColor[0], self.fgColor[1], self.fgColor[2]))
        self.image.blit(rendered_text, (self.spacing*2, -self.spacing))

    def drawFrame(self):
        pass
        # Makes a frame
        #self.fill(self.fg_color)
        #bg = pygame.Surface((self.W-(self.border*2), self.H-(self.border*2)))
        #
        #bg.fill(self.bg_color)
        #self.blit(bg, (self.border, self.border))

    def clicked(self):
        globs.focused = self

    def unfocus(self):
        globs.focused = None

class CharacterPreview(Sprite):
    def __init__(self, xy, wh):
        Sprite.__init__(self, xy, wh)
        self.image.fill((0,0,0))
        self.character_wh = (40,90)

        self.appearance = { 'hairstyle': "hair1", 'haircolor': (160,100,80), 'eyecolor': (0,0,0) }
        character_module = import_module("game.entities.character")
        self.Character = character_module.Character

        self.draw()

    def draw(self):
        self.image.fill((255,255,255))
        self.draw_character()

    def draw_character(self):
        self.character = self.Character((0,0), add=False, custom_appearance=self.appearance)
        #print(self.character.appearance)
        #self.character.rect.topleft = (x,y)
        tempSurface = Surface(self.character_wh)
        tempSurface.fill((255,255,255))
        self.character.blit(blitsurface=tempSurface)

        scaledCharacter = Surface((self.character_wh[0]*2, self.character_wh[1]*2))
        pygame.transform.scale2x(tempSurface, scaledCharacter)

        x = (self.rect.w/2) - (self.character_wh[0])
        y = (self.rect.h/2) - (self.character_wh[1])
        self.image.blit(scaledCharacter, (x,y))


class ListSelector(Sprite):
    def __init__(self, parent, xy, wh, selectionlist, text="Change this text", fontSize=None, spacing=5, bgColor=(0,0,0), fgColor=(255,255,255), alpha=250):
        Sprite.__init__(self, xy, wh)
        self.selectionlist = selectionlist
        self.parent = parent
        self.currentselection = 0
        self.text = text
        self.fontSize = fontSize
        self.fontFamily = 'calibri'
        self.bgColor = bgColor
        self.fgColor = fgColor
        self.alpha = alpha
        self.spacing = spacing
        self.currentcolor = (0,0,0)

        self.buttons = []

        self.loadFont()
        self.draw()
        self.draw_arrows()

    def draw(self):
        self.image.fill(self.bgColor)
        if self.alpha:
            self.image.set_alpha(self.alpha)
        print("Alpha:" +str(self.image.get_alpha()))
        self.draw_text()
        for button in self.buttons:
            print(button)
            print(button.rect.topleft)
            globs.screen.blit(button.image, button.rect.topleft)

    def draw_arrows(self):
        r = (self.rect.h/2)-self.spacing*2
        wh = (r,r)
        # Button next
        xy = (self.rect.x+self.spacing,
              self.rect.y+self.rect.h/2)
        button1 = Button(self.parent, xy, wh, text="<", bgColor=(255,255,255), borderRadius=3)
        button1.container = self
        button1.increment = -1
        # Button previous
        xy = (self.rect.x+self.spacing+r,
              self.rect.y+self.rect.h/2)
        button2 = Button(self.parent, xy, wh, text=">", bgColor=(255,255,255), borderRadius=3)
        button2.container = self
        button2.increment = 1
        # Button setup
        self.buttons.append(button1)
        self.buttons.append(button2)
        for button in self.buttons:
            def createCharacterButton_clicked(self):
                self.container.currentselection += self.increment
                if self.container.currentselection < 0:
                    self.container.currentselection = 0
                elif self.container.currentselection >= len(self.container.selectionlist):
                    self.container.currentselection = len(self.container.selectionlist)-1
                self.container.draw()
                #self.container.blit()
                try:
                    self.parent.characterPreview.appearance["hairstyle"] = self.container.selectionlist[self.container.currentselection]
                except IndexError:
                    self.container.currentselection -= self.increment
                self.parent.characterPreview.draw()
                print(str(self.increment) + " " + str(self.container.currentselection))
            button.onClick(createCharacterButton_clicked)

            button.parent.buttons.add(button)

    def draw_text(self):
        # Hairstyle text
        self.rendered_text_title = self.font.render(self.text, True, self.fgColor)
        self.rendered_text_title_xy = (self.rect.x+self.spacing, self.rect.y+self.spacing)
        # Hair name
        self.rendered_text_hairname = self.font.render(self.selectionlist[self.currentselection], True, self.fgColor)
        self.rendered_text_hairname_xy = (self.rect.x+self.rect.w/2-self.rendered_text_hairname.get_width()/2, self.rect.y+self.rect.w/2)
        print(self.rendered_text_hairname_xy)
        print(self.selectionlist[self.currentselection])

    def loadFont(self):
        if not self.fontSize:
            self.fontSize = (self.image.get_height()/2)-(self.spacing*4)
        self.font = globs.getFont(self.fontFamily, self.fontSize)

    def blit(self):
        Sprite.blit(self)
        globs.screen.blit(self.rendered_text_title, self.rendered_text_title_xy)
        globs.screen.blit(self.rendered_text_hairname, self.rendered_text_hairname_xy)



class ColorSelector(Sprite):
    def __init__(self, xy, wh, text="Change this text", fontSize=None, spacing=5, bgColor=(0,0,0), fgColor=(255,255,255), alpha=250):
        Sprite.__init__(self, xy, wh)
        self.text = text
        self.fontSize = fontSize
        self.fontFamily = 'calibri'
        self.bgColor = bgColor
        self.fgColor = fgColor
        self.alpha = alpha
        self.spacing = spacing
        self.currentcolor = (0,0,0)

        self.buttons = []

        self.loadFont()
        self.draw()

    def draw(self):
        self.image.fill(self.bgColor)
        if self.alpha:
            self.image.set_alpha(self.alpha)
        print("Alpha:" +str(self.image.get_alpha()))
        self.draw_currentcolor()
        self.draw_text()

    def draw_currentcolor(self):
        self.currentcolor_image = Surface((self.rect.h-self.spacing*2, self.rect.h-self.spacing*2))
        self.currentcolor_image_xy = (self.rect.x+self.spacing, self.rect.y+self.spacing)
        self.currentcolor_image.fill(self.currentcolor)

    def add_color(self, parent, color):
        r = (self.rect.h/2)-self.spacing*2
        xy = (self.currentcolor_image_xy[0]+self.currentcolor_image.get_width()+self.spacing+(len(self.buttons)*(r+self.spacing)),
              self.rect.y+self.rect.h/2)
        wh = (r,r)

        button = Button(parent, xy, wh, bgColor=color, borderRadius=wh[0]/2)
        button.container = self

        def createCharacterButton_clicked(self):
            self.container.currentcolor = self.bgColor
            self.container.draw()
            #self.container.blit()
            self.parent.characterPreview.appearance["haircolor"] = self.bgColor
            self.parent.characterPreview.draw()
        button.onClick(createCharacterButton_clicked)

        self.buttons.append(button)
        parent.buttons.add(button)

    def draw_text(self):
        self.rendered_text = self.font.render(self.text, True, self.fgColor)
        self.rendered_text_xy = (self.currentcolor_image_xy[0]+self.currentcolor_image.get_width()+self.spacing, self.rect.y+self.spacing)

    def loadFont(self):
        if not self.fontSize:
            self.fontSize = (self.image.get_height()/2)-(self.spacing*4)
        self.font = globs.getFont(self.fontFamily, self.fontSize)

    def blit(self):
        Sprite.blit(self)
        globs.screen.blit(self.currentcolor_image, self.currentcolor_image_xy)
        globs.screen.blit(self.rendered_text, self.rendered_text_xy)


class QuitButton(Button):
    def __init__(self, parent, xy, wh):
        Button.__init__(self, parent, xy, wh, (255, 255, 255), (0, 0, 0), "Quit", "calibri")
        self.draw()

    def clicked(self):
        globs.running = False


class BackButton(Button):
    def __init__(self, parent, back, xy, wh):
        Button.__init__(self, parent, xy, wh, (255, 255, 255), (0, 0, 0), "Back", "calibri")
        self.back = back
        self.draw()

    def clicked(self):
        globs.location = self.back
        if globs.focused:
            globs.focused.unfocus()