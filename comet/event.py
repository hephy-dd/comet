__all__ = ['Event']

class Event(object):

    def __init__(self):
        super().__init__()
        self.__targets = []

    def connect(self, target):
        if target not in self.__targets:
            self.__targets.append(target)

    def disconnect(self, target):
        self.__targets.remove(target)

    def emit(self, *args, **kwargs):
        for target in self.__targets:
            target(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.emit(*args, **kwargs)
