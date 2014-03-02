import pygame
import globals as globs

from game import Sprite

from menu.baseclasses import InputBox, TextBox, ButtonContainer, Button

class SystemMenu(ButtonContainer):
	def __init__(self, parent):
		text = "System Menu"
		wh = (200,300)
		xy = ((globs.resolution[0]/2)-(wh[0]/2), (globs.resolution[1]/2)-(wh[1]/2))
		self.hidden = True
		self.bgColor = (235,235,235)
		ButtonContainer.__init__(self, parent, xy, wh, text=text,
                		   bgColor=self.bgColor, buttonBgColor=(255,255,255), buttonFgColor=(0,0,0), buttonH=50, buttonSpacing=15)
		self.parent = globs.currentgame

		self.cutBorderRadius(15)
		self.drawText()

		def OptionsQuit(self):
			print("Not implemented yet")
		self.newButton('Options', OptionsQuit, self.buttons)

		def ClickQuit(self):
			globs.location = "menu.main"
			globs.focused = None
		self.newButton('Quit', ClickQuit, self.buttons)

		self.drawButtons()

	def drawButtons(self):
		for button in self.buttons:
			self.image.blit(button.image, button.localxy)

	def toggle(self):
		if self.hidden:
			globs.focused = self
			globs.currentgame.guiElements.add(self)
			#globs.currentgame.guiElements.add(self.buttons)
			globs.currentgame.buttons.add(self.buttons)
			self.hidden = False
		else:
			self.unfocus()
			globs.currentgame.guiElements.remove(self)
			#globs.currentgame.guiElements.remove(self.buttons)
			globs.currentgame.buttons.remove(self.buttons)
			self.hidden = True

	def unfocus(self):
		globs.focused = None


class ResourceBar(Button):
	def __init__(self, xy, wh, bgColor, fgColor, textColor=(0,0,0)):
		self.last = None
		self.percentageShow = False
		Button.__init__(self, globs.screen, xy, wh, bgColor=bgColor, fgColor=fgColor, text=None , fontsize=15, borderRadius=5)
		self.image.set_alpha(230)

	def update(self, value, maxvalue):
		self.maxvalue = maxvalue
		if self.last != value:
			self.last = value
			self.draw()

			percentage = self.last/float(self.maxvalue)
			#print(healthpercentage)

			healthImage = pygame.Surface((self.image.get_width()*percentage, self.image.get_height()))
			healthImage.fill(self.fgColor)
		
			self.image.blit(healthImage, (0, 0))
			#self.cutBorderRadius(self.borderRadius)

			if self.percentageShow:
				self.text = str(percentage*100) + "%"
			else:
				self.text = "{}/{}".format(value, maxvalue)
			self.drawText()

	def clicked(self):
		self.last = None
		self.percentageShow != self.percentageShow

'''

Chat related

'''

class ChatBubble(Sprite):
	def __init__(self, character):
		Sprite.__init__(self, (0,0), (100,30))
		self.owner = character
		globs.currentgame.guiElements.add(self)
		self.image.fill((0,0,0))

	def blit(self, screen):
		x = self.owner.rect.x-globs.cameraX-self.image.get_width()/2+self.owner.image.get_width()/2
		y = self.owner.rect.y-globs.cameraY-self.image.get_height()-10
		self.rect.topleft = (x, y)
		Sprite.blit(self, screen)

class ChatInputBox(InputBox):
	def __init__(self, xy, wh):
		InputBox.__init__(self, xy, wh, question=">", fgColor=(255,255,255), bgColor=(0,0,0), alpha=120)
		globs.currentgame.buttons.add(self)
		globs.currentgame.guiElements.add(self)
		self.baseAlpha = 120
		self.focusedAlpha = 180

	def clicked(self):
		globs.focused = self
		self.alpha = self.focusedAlpha
		self.draw()

		globs.currentgame.chatBox.alpha = globs.currentgame.chatBox.focusedAlpha
		globs.currentgame.chatBox.draw()

	def unfocus(self):
		globs.focused = None
		if self.inputText:
			globs.currentgame.chatBox.addEntry(globs.charactername, self.inputText)
			globs.currentgame.chatBox.draw()
			self.inputText = ""
		self.alpha = self.baseAlpha
		ChatBubble(globs.character)
		self.draw()

		globs.currentgame.chatBox.alpha = globs.currentgame.chatBox.baseAlpha
		globs.currentgame.chatBox.draw()

class ChatBox(TextBox):
	def __init__(self, xy, wh, rows):
		TextBox.__init__(self, xy, wh, rows, bgColor=(0,0,0), fgColor=(255,255,255), alpha=120, font='droidsansmono')
		self.baseAlpha = 120
		self.focusedAlpha = 180
		globs.currentgame.guiElements.add(self)

	def drawText(self):
		charcount = self.text.count('')
		charwidth = self.font.size('a')[0]
		chars_per_row = (self.image.get_width()/charwidth)

		entries = reversed(self.text.split('\n'))
		entrynum = len(self.text.split('\n'))
		rownum = self.rows-1
		for entry in entries:
			entrynum -= 1
			for row in reversed(range(((len(entry)/chars_per_row)+1))):
				text = entry[row*chars_per_row:(row+1)*chars_per_row]
				if text:
					#print(text)
					rendered_text = self.font.render(text, True, pygame.color.Color(self.fgColor[0], self.fgColor[1], self.fgColor[2]))
					self.image.blit(rendered_text, (self.spacing, self.spacing+(rownum*self.spacing)+(rownum*self.fontSize)))
					rownum -= 1

	def addEntry(self, name, message):
		self.text += "\n{}: {}".format(name, message)