from dataclasses import dataclass


@dataclass
class TempComparingUnit:
    before: any
    after: any
    all: any

    def __init__(self, before, after, everything=None):
        self.before = before
        self.after = after
        self.all = everything
