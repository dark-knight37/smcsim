from enum import Enum

class ProductKind(Enum):
    RED = 0
    BLUE = 1
    GREEN = 2
    YELLOW = 3
    BLACK = 4
    PURPLE = 5
    ORANGE = 6
    WHITE = 7


class MovementOrder(Enum):
    DRPI = 0
    DRPO = 1
    INBD = 2
    OUTD = 4

class StationDir(Enum):
    INPUT = 0
    OUTPUT = 1