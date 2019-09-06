class Keymap:
    def __init__(self, filename):
        self.tuples = [x.strip().split(",") for x in open(filename)]
        self.coefficient = dict(((x[0], x) for x in self.tuples))
        self.cal = dict(((x[1], x) for x in self.tuples))
        self.raw = dict(((x[2], x) for x in self.tuples))
