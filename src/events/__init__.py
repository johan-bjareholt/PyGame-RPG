import logging
import pygame

import globals as globs
from .eventtypes import *

logger = logging.getLogger("events")
eventlist = []

class Events:
    def __init__(self):
        self.logger = logging.getLogger("events")
        self.logger.info("Loading events")
        print("Loading events")
        eventlist.append(ClockEvent(10))

    def loop(self):
    	mode, sub = globs.location.split('.')
    	# Location based events
    	if mode == "menu":
    		pass
    	elif mode == "game":
    		pass

        # Timed Events
        for event in eventlist:
            eventtype = event.__class__.__name__
            if not event.isDone():
                logger.debug(str())
            else:
                eventlist.remove(event)
                print("Deleted " + str(event))

class Menus:
	def main(self):
		print("in main menu")

class Game:
	pass