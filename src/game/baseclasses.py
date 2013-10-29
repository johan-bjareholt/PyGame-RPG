import pygame
import globals as globs

from menu.baseclasses import InputBox, TextBox

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
					print(text)
					rendered_text = self.font.render(text, True, pygame.color.Color(self.fgColor[0], self.fgColor[1], self.fgColor[2]))
					self.image.blit(rendered_text, (self.spacing, self.spacing+(rownum*self.spacing)+(rownum*self.fontSize)))
					rownum -= 1

	def addEntry(self, name, message):
		self.text += "\n{}: {}".format(name, message)