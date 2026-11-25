# Singleton
class RestaurantManager:
    _instance = None

    def __init__(self):
        # private constructor
        self._restaurants = []

    @staticmethod
    def getInstance():
        if RestaurantManager._instance is None:
            RestaurantManager._instance = RestaurantManager()
        return RestaurantManager._instance

    def addRestaurant(self, r):
        self._restaurants.append(r)

    def searchByLocation(self, loc):
        result = []
        loc = loc.lower()
        for r in self._restaurants:
            rl = r.getLocation().lower()
            if rl == loc:
                result.append(r)
        return result
