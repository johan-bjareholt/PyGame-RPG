import pygame
import globals as globs

from menu.baseclasses import InputBox

class ChatBox(InputBox):
	def __init__(self, parent, xy, wh):
		InputBox.__init__(self, parent, xy, wh, question=">", fgColor=(255,255,255), bgColor=(0,0,0), alpha=120)

	def clicked(self):
		globs.focused = self

	def unfocus(self):
		globs.focused = None
		globs.currentgame.chatBox.text += self.inputText
		globs.currentgame.chatBox.draw()
		self.inputText = ""
		self.draw()