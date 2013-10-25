import pygame
import globals as globs


class Surface(pygame.Surface):
    '''
    Base class for surfaces
    '''
    def __init__(self, wh, transparent=False):
        if transparent:
            pygame.Surface.__init__(self, wh, pygame.RLEACCEL)
        else:
            pygame.Surface.__init__(self, wh)
        self.WH = wh
        self.W = self.WH[0]
        self.H = self.WH[1]


class Sprite(pygame.sprite.Sprite):
    '''
    Base class for sprites
    '''
    def __init__(self, parent, xy, wh, bgColor=None, colorkey=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface(wh)
        self.move(xy)
        self.parent = parent
        self.bgColor = bgColor
        self.colorkey = colorkey
        if self.bgColor:
            self.image.fill(self.bgColor)
        if colorkey:
            self.image.set_colorkey(self.transparent)

    def draw(self):
        pass

    def move(self, xy):
        self.xy = xy
        self.X, self.Y = self.xy
        self.rect = self.image.get_rect(topleft=self.xy)

    def blit(self):
        self.parent.blit(self.image, self.xy)

    def clicked(self):
        print("You just clicked me!")

    def rect(self):
        return self.get_rect(topleft=(self.X, self.Y))


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


def getFont(name, fontsize):
    fontlocation = globs.cwd + "/data/fonts/" + name + ".ttf"
    return pygame.font.Font(fontlocation, fontsize)