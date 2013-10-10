import logging
import pygame

import globals as globs
from .eventtypes import *

logger = logging.getLogger("events")

globs.eventlist = []

class Events:
    def __init__(self):
        self.logger = logging.getLogger("events")
        self.logger.info("Loading events")
        print("Loading events")
        #ClockTimer(10)

    def loop(self):
    	mode, sub = globs.location.split('.')
    	# Location based events
    	if mode == "menu":
    		pass
    	elif mode == "game":
    		pass

        # Timed Events
        for event in globs.eventlist:
            if not event.isDone():
                event.loop()
            else:
                globs.eventlist.remove(event)