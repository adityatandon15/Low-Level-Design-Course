from abc import ABC, abstractmethod


class IDataService(ABC):
    @abstractmethod
    def fetchData(self):
        pass


class RealDataService(IDataService):
    def __init__(self):
        # Imagine this connects to a remote server or loads heavy resources.
        print("[RealDataService] Initialized (simulating remote setup)")

    def fetchData(self):
        return "[RealDataService] Data from server"


# Remote proxy
class DataServiceProxy(IDataService):
    def __init__(self):
        self.realService = RealDataService()

    def fetchData(self):
        print("[DataServiceProxy] Connecting to remote service...")
        return self.realService.fetchData()


class RemoteProxy:
    @staticmethod
    def main(args):
        dataService = DataServiceProxy()
        dataService.fetchData()


if __name__ == "__main__":
    RemoteProxy.main([])
