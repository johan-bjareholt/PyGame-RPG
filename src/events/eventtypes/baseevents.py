import time
import globals as globs


class Event:
    '''
    All of the eventclasses baseclass
    '''
    def __init__(self):
        eventlist.append(self)


'''

Timed event classes

'''

class TimedEvent(Event):
    '''
    Base class for timed events
    '''

    def __init__(self, units):
        self.duration = units

    def __str__(self):
        return "{name} of {duration} {unit}s".format(name=str(self.__name__()), duration=str(self.duration), unit=self.unit)

    def isDone(self):
        # A function which returns True if 
        pass

    def loop(self):
        self.percentage = (self.endTime-self.startTime)/self.duration
        self.job()

    def job(self):
        # Do specific stuff here every loop
        pass


class ClockEvent(TimedEvent):
    '''
    Timed event where the duration is specified in floats of seconds
    '''
    def __name__(self):
        return "ClockEvent"

    def __init__(self, seconds):
        TimedEvent.__init__(self, seconds)
        self.unit = "second"
        self.startTime = time.time()
        self.endTime = time.time()+seconds

    def isDone(self):
        if time.time() > self.endTime:
            return True

    def loop(self):
        self.percentage = (self.endTime-self.startTime)/self.duration
        self.job()

    def job(self):
        # Do specific stuff here every loop
        pass


class FramedEvent(TimedEvent):
    '''
    Timed event where the duration is specified in number of frames
    '''
    def __init__(self, frames):
        Event.__init__(self, frames)
        self.frame = frames
        self.unit = "frame"

    def isDone(self):
        self.frame -= 1
        if self.frame:
            return True

    def loop(self):
        self.percentage = self.frame/self.duration
        self.job()

    def job():
        # Do specific stuff here every loop
        pass