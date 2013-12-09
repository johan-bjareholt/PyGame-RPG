import os
import ConfigParser

print("Initializing globals")

cwd = os.getcwd()
maindir = os.path.dirname(cwd)
datadir = cwd+"/data/"

config = ConfigParser.RawConfigParser()
def read_config():
	try:
		print('Loading settings conf')
		config.read("settings.conf")
	except Exception as e:
		print('Could not load settings file')
def write_config():
	with open('settings.conf', 'wb') as configfile:
		config.write(configfile)

read_config()

location = "menu.main"
lastlocation = ""
frame = 0
framecount = 0
framerate = 10

dirtyrects = []

online = False
connection = None

redraw = False
focused = None