from enum import Enum


class ApiFunction(Enum):
    INTRA_DAY = 1,
    DAILY = 2,
    WEEKLY = 3


class ApiInterval(Enum):
    Min1 = 1,
    Min5 = 5,
    Min15 = 15,
    Min30 = 30,
    Min60 = 60
