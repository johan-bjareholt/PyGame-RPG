import pygame
import os
screensize = (1280, 720)

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


class Menu(Surface):
    def __init__(self, background="/sky.jpg"):
        Surface.__init__(self, (0, 0), screensize)
        if background:
            self.backgroundImage = pygame.image.load(os.getcwd()+background)
            self.backgroundImage = pygame.transform.scale(self.backgroundImage, screensize)
            print(self.backgroundImage)
            self.background = self.subsurface(self.backgroundImage)
        else:
            self.background = Surface((0, 0), screensize, color=(0, 0, 0))
        self.blit(self.background, (0, 0))

class MainMenu(Menu):
    def __init__(self):
        Menu.__init__(self)


class Button(Surface):
    def __init__(self, xy, wh, color=(255, 255, 255)):
        Surface.__init__(self, xy, wh)

    def rect(self):
        return self.get_rect(topleft=(self.X, self.Y))
