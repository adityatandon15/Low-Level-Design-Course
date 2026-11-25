from datetime import datetime


class TimeUtils:
    @staticmethod
    def getCurrentTime():
        now = datetime.now()
        return now.strftime("%a %b %d %H:%M:%S %Y")
