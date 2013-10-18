import os

print("Initializing globals")
resolution = (1280, 720)
location = "menu.main"
cwd = os.getcwd()
frame = 0
framecount = 0
framerate = 10

redraw = False
focusedtextbox = None