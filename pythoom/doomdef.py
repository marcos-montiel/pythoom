from enum import Enum, auto


class GameMode(Enum):
    Shareware = (auto(),)
    Registered = (auto(),)
    Commercial = (auto(),)
    Retail = (auto(),)
    Indetermined = auto()


class Languages(Enum):
    English = (auto(),)
    French = (auto(),)
    German = (auto(),)
    Unknown = auto()
