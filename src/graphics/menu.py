import pygame
import os
screensize = (1280, 720)

def getFont(name):
    return os.getcwd() + "/graphics/fonts/" + name + ".ttf"

class Surface(pygame.Surface):
    def __init__(self, xy, wh, color=None, transparent=False, background=None):
        pygame.Surface.__init__(self, (wh))
        self.XY = xy
        self.X = self.XY[0]
        self.Y = self.XY[1]
        self.WH = wh
        self.W = self.WH[0]
        self.H = self.WH[1]
        self.color = color
        if color:
            self.fill(color)

    def rect(self):
        return self.get_rect(topleft=(self.X, self.Y))

class Menu(Surface):
    def __init__(self, bgImage="/sky.jpg", bgColor=(0, 0, 0), font="calibri"):
        Surface.__init__(self, (0, 0), screensize)

        self.background = self.subsurface((0, 0), screensize)
        self.main = self.subsurface((0, 0), screensize)
        self.foreground = self.subsurface((0, 0), screensize)

        # Background initialization
        if bgImage:
            self.backgroundImage = pygame.image.load(os.getcwd()+bgImage)
            self.backgroundImage = pygame.transform.scale(self.backgroundImage, screensize)
        self.backgroundColor = bgColor

        self.fontname = font
        self.fontlocation = getFont(font)


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

        self.blitBackground()
        self.blitMain()
        self.blitForeground()


class MainMenu(Menu):
    def __init__(self):
        Menu.__init__(self)

    def drawMain(self):
        self.button1 = Button((25, 100), (100, 25), text="Hello")
        self.button1.draw()

    def blitMain(self):
        self.main.blit(self.button1, self.button1.XY)

class Button(Surface):
    def __init__(self, xy, wh, bgColor=(255, 255, 255), fgColor=(0, 0, 0), text=None, font="calibri"):
        Surface.__init__(self, xy, wh)
        self.bgColor = bgColor
        self.fgColor = fgColor
        self.text = text
        self.fontname = font

    def draw(self):
        # Fill background
        self.fill(self.bgColor)
        # Apply text
        if self.text:
            self.fontsize = self.H/2 + 10
            self.fontlocation = getFont(self.fontname)
            self.font = pygame.font.Font((self.fontlocation), self.fontsize)
            self.renderedText = self.font.render(self.text, True, pygame.color.Color(0,0,0))
            # Centered text
            x = (self.W-self.renderedText.get_width())/2
            y = (self.H-self.fontsize)/2
            self.blit(self.renderedText, (x, y))
