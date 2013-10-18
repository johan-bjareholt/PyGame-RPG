from graphics.baseclasses import *


class Menu(Surface):
    '''
    Base class for the menus
    '''
    def __init__(self, bgImage="/sky.jpg", bgColor=(0, 0, 0), font="calibri"):
        Surface.__init__(self, globs.resolution)

        self.background = self.subsurface((0, 0), globs.resolution)
        self.main = self.subsurface((0, 0), globs.resolution)
        self.foreground = self.subsurface((0, 0), globs.resolution)

        self.buttons = pygame.sprite.Group()

        # Background initialization
        if bgImage:
            self.backgroundImage = pygame.image.load(globs.cwd+bgImage)
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

    # Foreground layer
    def drawForeground(self):
        pass

    def blitForeground(self):
        pass

    # Main commands
    def draw(self):
        self.drawBackground()
        self.drawMain()
        self.drawForeground()

    def blitz(self):
        self.blitBackground()
        self.blitMain()
        self.blitForeground()






class Container(Sprite):
    def __init__(self, parent, xy, wh, bgColor=None, text=None):
        Sprite.__init__(self, parent, xy, wh, bgColor=(235,235,255))
        self.text = text
        self.drawText()

    def drawText(self):
        if self.text:
            self.textSprite = Text(self, (10,10), self.text, 25)
            self.image.blit(self.textSprite.image, self.textSprite.xy)


class Button(Sprite):
    def __init__(self, parent, xy, wh, bgColor=(255, 255, 255), fgColor=(0, 0, 0), text=None, font="calibri", fontsize=None):
        Sprite.__init__(self, parent, xy, wh, bgColor)

        self.fgColor = fgColor
        self.text = text
        self.fontname = font
        self.fontsize = fontsize
        self.draw()

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
                self.fontsize = self.image.H/2
            # Load font
            self.font = getFont(self.fontname, self.fontsize)
            self.renderedText = self.font.render(self.text, True, pygame.color.Color(0, 0, 0))
            # Center text
            x = (self.image.W-self.renderedText.get_width())/2
            y = (self.image.H-self.fontsize)/2
            # Blit to sprites surface
            self.image.blit(self.renderedText, (x, y))

    def clicked(self):
        print("You just clicked me!")


class TextBox(Sprite):
    def __init__(self, parent, xy, wh, question="", fgColor=(0, 0, 0), bgColor=(255, 255, 255)):
        Sprite.__init__(self, parent, xy, wh, bgColor)
        self.bgColor = bgColor
        self.fgColor = fgColor
        self.question = question
        self.inputText = ""
        self.focus = False
        self.loadFont()
        self.draw()

    def draw(self):
        self.image.fill(self.bgColor)
        self.drawFrame()
        self.drawText()

    def loadFont(self):
        self.fontSize = self.image.get_height()-4
        self.font = pygame.font.Font(globs.cwd+"/graphics/fonts/calibri.ttf", self.fontSize)

    def drawText(self):
        text = self.question + self.inputText
        rendered_text = self.font.render(text, True, pygame.color.Color(0, 0, 0))
        #"Singleplayer", True, pygame.color.Color(0, 0, 0)
        #self.blit(rendered_text, (self.XY_textStart, self.XY_textStart))
        self.image.blit(rendered_text, (4,0))

    def drawFrame(self):
        pass
        # Makes a frame
        #self.fill(self.fg_color)
        #bg = pygame.Surface((self.W-(self.border*2), self.H-(self.border*2)))
        #
        #bg.fill(self.bg_color)
        #self.blit(bg, (self.border, self.border))

    def clicked(self):
        globs.focusedtextbox = self


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