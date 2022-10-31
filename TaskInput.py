from dataclasses import dataclass


@dataclass
class TaskInput:
    month_order: int
    name: str

    def __init__(self, name: str, month_order: any):
        self.name = name
        self.month_order = month_order
