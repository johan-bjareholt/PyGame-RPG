import os

print("Initializing globals")
resolution = (1280, 720)
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