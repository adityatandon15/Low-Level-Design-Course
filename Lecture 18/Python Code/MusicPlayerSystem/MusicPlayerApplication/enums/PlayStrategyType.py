from enum import Enum, auto


class PlayStrategyType(Enum):
    SEQUENTIAL = auto()
    RANDOM = auto()
    CUSTOM_QUEUE = auto()
