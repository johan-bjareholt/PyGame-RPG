import pygame
import globals as globs

class Surface(pygame.Surface):
    '''
    Base class for surfaces
    '''
    def __init__(self, wh, transparent=False, bgColor=None):
        pygame.Surface.__init__(self, (wh))
        self.WH = wh
        self.W = self.WH[0]
        self.H = self.WH[1]
        if bgColor:
            self.fill(bgColor)

    def rect(self):
        return self.get_rect(topleft=(self.X, self.Y))

class Sprite(pygame.sprite.Sprite):
    '''
    Base class for sprites
    '''
    def __init__(self, parent, xy, wh, bgColor=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface(wh)
        self.xy = xy
        self.parent = parent
        self.rect = self.image.get_rect(topleft=xy)
        self.bgColor = bgColor
        if self.bgColor:
            self.image.fill(self.bgColor)

    def draw(self):
        pass

    def blit(self):
        self.parent.blit(self.image, (self.xy))

    def clicked(self):
        print("You just clicked me!")

class Text(Sprite):
    def __init__(self, parent, xy, text, size, color=(0, 0, 0), font="calibri"):
        self.font = getFont(font, size)
        self.color = color
        self.text = text
        self.draw()
        wh = self.renderedText.get_size()
        Sprite.__init__(self, parent, xy, wh)
        self.image = self.renderedText

    def draw(self):
        self.renderedText = self.font.render(self.text, True, pygame.color.Color(self.color[0], self.color[1], self.color[2]))

class Button(Sprite):
    def __init__(self, parent, xy, wh, bgColor=(255, 255, 255), fgColor=(0, 0, 0), text=None, font="calibri"):
        Sprite.__init__(self, parent, xy, wh, bgColor)

        self.fgColor = fgColor
        self.text = text
        self.fontname = font

    def draw(self):
        # Fill background
        self.image.fill(self.bgColor)
        # Apply text
        if self.text:
            # Adapt fontsize
            self.fontsize = self.image.H/2 + 10
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



def getFont(name, fontsize):
    fontlocation = globs.cwd + "/graphics/fonts/" + name + ".ttf"
    return pygame.font.Font(fontlocation, fontsize)