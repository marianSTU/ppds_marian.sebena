from fei.ppds import Thread


class Shared:
    def __init__(self, size):
        self.counter = 0
        self.end = size
        self.elms = [0]
