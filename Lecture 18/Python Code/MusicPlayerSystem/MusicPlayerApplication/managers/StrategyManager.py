import threading

from ..enums.PlayStrategyType import PlayStrategyType
from ..strategies.CustomQueueStrategy import CustomQueueStrategy
from ..strategies.RandomPlayStrategy import RandomPlayStrategy
from ..strategies.SequentialPlayStrategy import SequentialPlayStrategy


class StrategyManager:
    instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.sequentialStrategy = SequentialPlayStrategy()
        self.randomStrategy = RandomPlayStrategy()
        self.customQueueStrategy = CustomQueueStrategy()

    @staticmethod
    def getInstance():
        with StrategyManager._lock:
            if StrategyManager.instance is None:
                StrategyManager.instance = StrategyManager()
            return StrategyManager.instance

    def getStrategy(self, type):
        if type == PlayStrategyType.SEQUENTIAL:
            return self.sequentialStrategy
        elif type == PlayStrategyType.RANDOM:
            return self.randomStrategy
        else:
            return self.customQueueStrategy
