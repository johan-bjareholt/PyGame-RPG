import time
import globals as globs

from graphics.baseclasses import Text

class Event:
    '''
    All of the eventclasses baseclass
    '''
    def __name__(self):
        return "BaseEvent"
    def __init__(self):
        globs.eventlist.append(self)
    def isDone(self):
        # A function which returns True if it is done
        pass

    def loop(self):
        # Do this every frame
        pass

    def load(self):
        # Do loading stuff
        pass

    def quit(self):
        # Do quit stuff
        pass

    def job(self):
        # Do specific stuff here every loop
        pass

'''

Timed event classes

'''


class ClockTimer(Event):
    '''
    Timed event where the duration is specified in floats of seconds
    '''
    def __name__(self):
        return "ClockEvent"

    def __init__(self, seconds):
        Event.__init__(self)
        self.duration = seconds
        self.startTime = time.time()
        self.endTime = time.time()+self.duration
        self.load()

    def isDone(self):
        if time.time() > self.endTime:
            self.quit()
            return True

    def loop(self):
        self.percentage = (self.endTime-self.startTime)/self.duration
        self.job()

    def load(self):
        # Do load stuff
        pass

    def quit(self):
        # Do quit stuff
        pass

    def job(self):
        # Do specific stuff here every loop
        pass


class FrameTimer(Event):
    '''
    Timed event where the duration is specified in number of frames
    '''
    def __name__(self):
        return "FramedEvent"

    def __init__(self, frames):
        Event.__init__(self)
        self.duration = frames
        self.frame = frames
        self.unit = "frame"
        self.load()

    def isDone(self):
        self.frame -= 1
        if self.frame:
            self.quit()
            return True

    def loop(self):
        self.percentage = self.frame/self.duration
        self.job()

    def load(self):
        # Do load stuff
        pass

    def quit(self):
        # Do quit stuff
        pass

    def job():
        # Do specific stuff here every loop
        pass

class FpsCounter(ClockTimer):
    def __name__(self):
        return "FpsCounterEvent"

    def __init__(self, lastframecount=0):
        ClockTimer.__init__(self, 1)
        self.framecount = 0

    def loop(self):
        self.framecount += 1

    def quit(self):
        # Do quit stuff
        globs.framecount = self.framecount
        FpsCounter(self.framecount)