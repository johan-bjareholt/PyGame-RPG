import os
import sys
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
		sys.exit('Could not load settings file')

def load_config():
	if config.get("dev", "dirtyrects") == "True":
		dirtyrects = True
	else:
		dirtyrects = False

def write_config():
	with open('settings.conf', 'wb') as configfile:
		config.write(configfile)

read_config()
load_config()

location = "menu.main"
lastlocation = ""
frame = 0
framecount = 0
framerate = 10

dirtyrects = []

charactername = ""

online = False
connection = None

redraw = False
focused = None