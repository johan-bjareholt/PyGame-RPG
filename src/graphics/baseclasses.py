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
    def __init__(self, parent, xy, wh, bgColor=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface(wh)
        self.move(xy)
        self.parent = parent
        self.bgColor = bgColor
        if self.bgColor:
            self.image.fill(self.bgColor)

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

class Container(Sprite):
    def __init__(self, parent, xy, wh, bgColor=None, text=None):
        Sprite.__init__(self, parent, xy, wh, bgColor=(235,235,255))
        self.text = text
        self.drawText()

    def drawText(self):
        if self.text:
            self.textSprite = Text(self, (10,10), self.text, 25)
            self.image.blit(self.textSprite.image, self.textSprite.xy)


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
    def __init__(self, parent, xy, wh, bgColor=(255, 255, 255), fgColor=(0, 0, 0), text=None, font="calibri", fontsize=None):
        Sprite.__init__(self, parent, xy, wh, bgColor)

        self.fgColor = fgColor
        self.text = text
        self.fontname = font
        self.fontsize = fontsize
        self.draw()

    def draw(self):
        # Fill background
        self.image.fill(self.bgColor)
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

class QuitButton(Button):
    def __init__(self, parent, xy, wh):
        Button.__init__(self, parent, xy, wh, (255, 255, 255), (0, 0, 0), "Quit", "calibri")
        self.draw()

    def clicked(self):
        pygame.quit()

class BackButton(Button):
    def __init__(self, back, parent, xy, wh):
        Button.__init__(self, parent, xy, wh, (255, 255, 255), (0, 0, 0), "Back", "calibri")
        self.back = back
        self.draw()

    def clicked(self):
        globs.location = self.back

def getFont(name, fontsize):
    fontlocation = globs.cwd + "/graphics/fonts/" + name + ".ttf"
    return pygame.font.Font(fontlocation, fontsize)