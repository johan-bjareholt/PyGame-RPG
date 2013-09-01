from baseevents import Event

class PersistentGameEvent(Event):
    '''
    A Persistent event while in-game
    '''
    def isDone(self):
        if 'menu' == globs.location.split('.')[0]:
            return True
        return False
