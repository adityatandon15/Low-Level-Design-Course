# Flyweight - Stores INTRINSIC state only
class AsteroidFlyweight:
    # Intrinsic properties (shared among asteroids of same type)
    def __init__(self, l, w, wt, col, tex, mat):
        self.length = l
        self.width = w
        self.weight = wt
        self.color = col
        self.texture = tex
        self.material = mat

    def render(self, posX, posY, velocityX, velocityY):
        print("Rendering " + self.color + ", " + self.texture + ", " + self.material
            + " asteroid at (" + str(posX) + "," + str(posY)
            + ") Size: " + str(self.length) + "x" + str(self.width)
            + " Velocity: (" + str(velocityX) + ", "
            + str(velocityY) + ")")

    @staticmethod
    def getMemoryUsage():
        # Integer.BYTES * 3 (length, width, weight) + approximate string data
        return 4 * 3 + 40 * 3


# Flyweight Factory
class AsteroidFactory:
    flyweights = {}

    @staticmethod
    def getAsteroid(length, width, weight, color, texture, material):
        key = (str(length) + "_" + str(width) + "_" + str(weight) + "_"
               + color + "_" + texture + "_" + material)

        if key not in AsteroidFactory.flyweights:
            AsteroidFactory.flyweights[key] = AsteroidFlyweight(
                length, width, weight, color, texture, material)

        return AsteroidFactory.flyweights[key]

    @staticmethod
    def getFlyweightCount():
        return len(AsteroidFactory.flyweights)

    @staticmethod
    def getTotalFlyweightMemory():
        return len(AsteroidFactory.flyweights) * AsteroidFlyweight.getMemoryUsage()

    @staticmethod
    def cleanup():
        AsteroidFactory.flyweights.clear()


# Context - Stores EXTRINSIC state only
class AsteroidContext:
    def __init__(self, fw, posX, posY, velX, velY):
        self.flyweight = fw
        self.posX = posX          # position
        self.posY = posY
        self.velocityX = velX     # velocity
        self.velocityY = velY

    def render(self):
        self.flyweight.render(self.posX, self.posY, self.velocityX, self.velocityY)

    @staticmethod
    def getMemoryUsage():
        return 8 + 4 * 4  # approximate pointer + Integer.BYTES * 4


class SpaceGameWithFlyweight:
    def __init__(self):
        self.asteroids = []

    def spawnAsteroids(self, count):
        print("\n=== Spawning " + str(count) + " asteroids ===")

        colors = ["Red", "Blue", "Gray"]
        textures = ["Rocky", "Metallic", "Icy"]
        materials = ["Iron", "Stone", "Ice"]
        sizes = [25, 35, 45]

        for i in range(count):
            type_ = i % 3

            flyweight = AsteroidFactory.getAsteroid(
                sizes[type_], sizes[type_], sizes[type_] * 10,
                colors[type_], textures[type_], materials[type_]
            )

            self.asteroids.append(AsteroidContext(
                flyweight,
                100 + i * 50,  # Simple x: 100, 150, 200, 250...
                200 + i * 30,  # Simple y: 200, 230, 260, 290...
                1,             # All move right with velocity 1
                2              # All move down with velocity 2
            ))

        print("Created " + str(len(self.asteroids)) + " asteroid contexts")
        print("Total flyweight objects: " + str(AsteroidFactory.getFlyweightCount()))

    def renderAll(self):
        print("\n--- Rendering first 5 asteroids ---")
        for i in range(min(5, len(self.asteroids))):
            self.asteroids[i].render()

    def calculateMemoryUsage(self):
        contextMemory = len(self.asteroids) * AsteroidContext.getMemoryUsage()
        flyweightMemory = AsteroidFactory.getTotalFlyweightMemory()
        return contextMemory + flyweightMemory

    def getAsteroidCount(self):
        return len(self.asteroids)


class WithFlyWeight:
    @staticmethod
    def main(args):
        ASTEROID_COUNT = 1_000_000

        print("\nTESTING WITH FLYWEIGHT PATTERN")
        game = SpaceGameWithFlyweight()

        game.spawnAsteroids(ASTEROID_COUNT)

        # Show first 5 asteroids to see the pattern
        game.renderAll()

        # Calculate and display memory usage
        totalMemory = game.calculateMemoryUsage()

        print("\n=== MEMORY USAGE ===")
        print("Total asteroids: " + str(ASTEROID_COUNT))
        print("Memory per asteroid: " + str(AsteroidContext.getMemoryUsage()) + " bytes")
        print("Total memory used: " + str(totalMemory) + " bytes")
        print("Memory in MB: " + str(totalMemory / (1024.0 * 1024.0)) + " MB")


if __name__ == "__main__":
    import sys
    WithFlyWeight.main(sys.argv[1:])
