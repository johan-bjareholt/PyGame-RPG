import pygame
import globals as globs

from menu.baseclasses import InputBox, TextBox, Container

class ChatInputBox(InputBox):
	def __init__(self, parent, xy, wh):
		InputBox.__init__(self, parent, xy, wh, question=">", fgColor=(255,255,255), bgColor=(0,0,0), alpha=120)
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
		self.draw()

		globs.currentgame.chatBox.alpha = globs.currentgame.chatBox.baseAlpha
		globs.currentgame.chatBox.draw()

class ChatBox(TextBox):
	def __init__(self, parent, xy, wh, rows):
		TextBox.__init__(self, parent, xy, wh, rows, bgColor=(0,0,0), fgColor=(255,255,255), alpha=120)
		self.baseAlpha = 120
		self.focusedAlpha = 180

	def drawText(self):
		charcount = self.text.count('')
		charwidth = self.font.size('a')[0]
		chars_per_row = (self.image.get_width()/charwidth)

		entries = reversed(self.text.split('\n'))
		entrynum = len(self.text.split('\n'))
		rownum = self.rows-1
		for entry in entries:
			entrynum -= 1
			for row in range(((len(entry)/chars_per_row)+1)):
				text = entry[row*chars_per_row:(row+1)*chars_per_row]
				if text:
					#print(text)
					rendered_text = self.font.render(text, True, pygame.color.Color(self.fgColor[0], self.fgColor[1], self.fgColor[2]))
					self.image.blit(rendered_text, (self.spacing, self.spacing+(rownum*self.spacing)+(rownum*self.fontSize)))
					rownum -= 1

	def addEntry(self, name, message):
		self.text += "\n{}: {}".format(name, message)

class SystemMenu(Container):
	def __init__(self, asd):
		text = "System Menu"
		wh = (200,300)
		xy = ((globs.resolution[0]/2)-(wh[0]/2), (globs.resolution[1]/2)-(wh[1]/2))
		self.hidden = True
		Container.__init__(self, globs.screen, xy, wh, text=text,
                		   bgColor=(235,235,235), buttonBgColor=(255,255,255), buttonFgColor=(0,0,0), buttonH=50, buttonSpacing=15)
		self.parent = globs.currentgame

		self.cutBorderRadius(15)
		self.drawText()

		def OptionsQuit(self):
			print("Not implemented yet")
		self.newButton('Options', OptionsQuit)

		def ClickQuit(self):
			globs.location = "menu.main"
		self.newButton('Quit', ClickQuit)

		self.drawButtons()

	def drawButtons(self):
		for button in self.buttons:
			print(button)
			self.image.blit(button.image, button.localxy)

	def toggle(self):
		if self.hidden:
			globs.currentgame.guiElements.add(self)
			#globs.currentgame.guiElements.add(self.buttons)
			#globs.currentgame.buttons.add(self.buttons)
			self.hidden = False
		else:
			globs.currentgame.guiElements.remove(self)
			#globs.currentgame.guiElements.remove(self.buttons)
			#globs.currentgame.buttons.remove(self.buttons)
			self.hidden = True