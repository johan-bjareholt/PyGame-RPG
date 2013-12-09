from graphics.baseclasses import *
import types


class Menu(Surface):
    '''
    Base class for the menus
    '''
    def __init__(self, bgImage="/menubackground.jpg", bgColor=(0, 0, 0), font="calibri"):
        Surface.__init__(self, globs.resolution)

        self.background = self.subsurface((0, 0), globs.resolution)
        self.main = self.subsurface((0, 0), globs.resolution)
        self.foreground = self.subsurface((0, 0), globs.resolution)

        self.buttons = pygame.sprite.Group()

        # Background initialization
        if bgImage:
            self.backgroundImage = pygame.image.load(globs.datadir+bgImage)
            self.backgroundImage = pygame.transform.scale(self.backgroundImage, globs.resolution)
        self.backgroundColor = bgColor

        self.fontname = font

    # Background layer
    def drawBackground(self):
        if self.backgroundImage:
            self.background.blit(self.backgroundImage, (0, 0))
        else:
            self.background.fill(self.backgroundColor)

    def blitBackground(self):
        pass

    # Main layer
    def drawMain(self):
        pass

    def blitMain(self):
        pass

    # Main commands
    def draw(self):
        self.drawBackground()
        self.drawMain()

    def blitz(self):
        self.blitBackground()
        self.blitMain()


class Container(Sprite):
    def __init__(self, parent, xy, wh, bgColor=(235,235,235), text='', textsize=10, spacing=2):
        Sprite.__init__(self, parent, xy, wh, bgColor=bgColor)
        self.text = text
        self.spacing = spacing
        self.entries = []

    def draw(self):
        x = 10
        y = self.spacing

        # Draw text
        self.textSprite = Text(self, x, y, self.textsize)

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
        Sprite.__init__(self, parent, xy, wh, bgColor=bgColor)
        self.text = text

        self.buttons = []
        self.buttonH = buttonH
        self.buttonSpacing = buttonSpacing
        self.buttonBgColor = buttonBgColor
        self.buttonFgColor = buttonFgColor

        self.drawText()
        self.updateButtons()

    def drawText(self):
        self.textSprite = Text(self, (10,10), self.text, 25)
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
        self.parent.buttons.add(newbutton)
        return newbutton

class Button(Sprite):
    def __init__(self, parent, xy, wh, bgColor=(255, 255, 255), fgColor=(0, 0, 0), text=None, font="calibri", fontsize=None, borderRadius=5):
        Sprite.__init__(self, parent, xy, wh, bgColor)

        self.fgColor = fgColor
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
            # Adapt fontsize
            if not self.fontsize:
                self.fontsize = (self.image.get_height()/2)+2
            # Load font
            self.font = globs.getFont(self.fontname, self.fontsize)
            self.renderedText = self.font.render(self.text, True, pygame.color.Color(0, 0, 0))
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
    def __init__(self, parent, xy, wh, rows, spacing=3, font='calibri', fgColor=(0, 0, 0), bgColor=(255, 255, 255), alpha=None, reverse=False):
        Sprite.__init__(self, parent, xy, wh, bgColor, alpha=alpha)
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
    def __init__(self, parent, xy, wh, question="", fgColor=(0, 0, 0), bgColor=(255, 255, 255), alpha=None, font='droidsansmono', fontSize=None, spacing=2):
        Sprite.__init__(self, parent, xy, wh, bgColor)
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

class QuitButton(Button):
    def __init__(self, parent, xy, wh):
        Button.__init__(self, parent, xy, wh, (255, 255, 255), (0, 0, 0), "Quit", "calibri")
        self.draw()

    def clicked(self):
        globs.running = False


class BackButton(Button):
    def __init__(self, back, parent, xy, wh):
        Button.__init__(self, parent, xy, wh, (255, 255, 255), (0, 0, 0), "Back", "calibri")
        self.back = back
        self.draw()

    def clicked(self):
        globs.location = self.back
        if globs.focused:
            globs.focused.unfocus()