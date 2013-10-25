from graphics.baseclasses import *


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
                self.fontsize = (self.image.H/2)+2
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
    def __init__(self, parent, xy, wh, rows, spacing=3, fgColor=(0, 0, 0), bgColor=(255, 255, 255), alpha=None):
        Sprite.__init__(self, parent, xy, wh, bgColor)
        self.bgColor = bgColor
        self.fgColor = fgColor
        self.alpha = alpha
        self.text = "Testing testing 123 123 hello there i love ponies and so should you! like a baws man"
        self.focus = False
        self.rows = rows
        self.spacing = spacing

        self.loadFont()
        self.draw()

    def draw(self):
        self.image.fill(self.bgColor)
        if self.alpha:
            self.image.set_alpha(self.alpha)
        self.drawFrame()
        self.drawText()

    def loadFont(self):
        totalspacing = self.spacing*self.rows+self.spacing
        self.fontSize = (self.image.get_height()-totalspacing)/self.rows
        #self.fontSize = self.image.get_height()-4
        self.font = getFont('calibri', self.fontSize)

    def drawText(self):
        textwidth = self.font.size(self.text)[0]
        self.characters_per_row = (self.image.get_width()-(self.spacing*2)) / (textwidth/self.text.count(''))
        print("Width:"+str(self.image.get_width()))
        print("spacing:"+str(self.spacing))
        print("textwidth:"+str(textwidth))
        print("total chars:"+str(self.text.count('')))
        print("cpr:"+str(self.characters_per_row))
        for row in range((self.text.count('')/self.characters_per_row)+1):
            text = self.text[row*self.characters_per_row:row*(self.characters_per_row)+self.characters_per_row]
            print(row)
            print(text)
            rendered_text = self.font.render(text, True, pygame.color.Color(self.fgColor[0], self.fgColor[1], self.fgColor[2]))
            self.image.blit(rendered_text, (self.spacing,self.spacing+(row*self.spacing)+(row*self.fontSize)))
        #rendered_text = self.font.render(text, True, pygame.color.Color(self.fgColor[0], self.fgColor[1], self.fgColor[2]))
        #self.image.blit(rendered_text, (4,0))

    def drawFrame(self):
        pass

class InputBox(Sprite):
    def __init__(self, parent, xy, wh, question="", fgColor=(0, 0, 0), bgColor=(255, 255, 255), alpha=None, fontSize=None):
        Sprite.__init__(self, parent, xy, wh, bgColor)
        self.bgColor = bgColor
        self.fgColor = fgColor
        self.alpha = alpha
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
            self.fontSize = self.image.H-4
        self.font = getFont('calibri', self.fontSize)

    def drawText(self):
        text = self.question + self.inputText
        rendered_text = self.font.render(text, True, pygame.color.Color(self.fgColor[0], self.fgColor[1], self.fgColor[2]))
        #"Singleplayer", True, pygame.color.Color(0, 0, 0)
        #self.blit(rendered_text, (self.XY_textStart, self.XY_textStart))
        self.image.blit(rendered_text, ((self.image.get_height()-self.fontSize)/2, (self.image.get_height()-self.fontSize)/2))

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

def getFont(name, fontsize):
    fontlocation = globs.cwd + "/data/fonts/" + name + ".ttf"
    return pygame.font.Font(fontlocation, fontsize)