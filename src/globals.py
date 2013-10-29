import os
import ConfigParser

print("Initializing globals")

try:
	print('Loading settings conf')
	config = ConfigParser.ConfigParser()
	config.read("settings.conf")
except Exception as e:
	print('Could not load settings file')

#resolution = (1280, 720)
location = "menu.main"
lastlocation = ""
cwd = os.getcwd()
datadir = cwd+"/data/"
frame = 0
framecount = 0
framerate = 10

online = False

redraw = False
focused = None