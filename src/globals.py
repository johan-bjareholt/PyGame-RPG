import os
import ConfigParser

print("Initializing globals")

cwd = os.getcwd()
maindir = os.path.dirname(cwd)
datadir = cwd+"/data/"

try:
	print('Loading settings conf')
	config = ConfigParser.ConfigParser()
	config.read("settings.conf")
except Exception as e:
	print('Could not load settings file')

location = "menu.main"
lastlocation = ""
frame = 0
framecount = 0
framerate = 10

dirtyrects = []

online = False

redraw = False
focused = None