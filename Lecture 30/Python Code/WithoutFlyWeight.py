class Asteroid:
    # Intrinsic properties (same for many asteroids) - DUPLICATED FOR EACH OBJECT
    # Extrinsic properties (unique for each asteroid)
    def __init__(self, l, w, wt, col, tex, mat, posX, posY, velX, velY):
        self.length = l
        self.width = w
        self.weight = wt
        self.color = col
        self.texture = tex
        self.material = mat
        self.posX = posX
        self.posY = posY
        self.velocityX = velX
        self.velocityY = velY

    def render(self):
        print("Rendering " + self.color + ", " + self.texture + ", " + self.material
            + " asteroid at (" + str(self.posX) + "," + str(self.posY)
            + ") Size: " + str(self.length) + "x" + str(self.width)
            + " Velocity: (" + str(self.velocityX) + ", "
            + str(self.velocityY) + ")")

    # Calculate approximate memory usage per object
    @staticmethod
    def getMemoryUsage():
        # Integer.BYTES * 7 (length, width, weight, x, y, velocityX, velocityY)
        # + approximate string data (assuming average 10 chars each)
        return 4 * 7 + 40 * 3


class SpaceGame:
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

            self.asteroids.append(Asteroid(
                sizes[type_], sizes[type_], sizes[type_] * 10,
                colors[type_], textures[type_], materials[type_],
                100 + i * 50,         # Simple x: 100, 150, 200, 250...
                200 + i * 30,         # Simple y: 200, 230, 260, 290...
                1,                    # All move right with velocity 1
                2                     # All move down with velocity 2
            ))

        print("Created " + str(len(self.asteroids)) + " asteroid objects")

    def renderAll(self):
        print("\n--- Rendering first 5 asteroids ---")
        for i in range(min(5, len(self.asteroids))):
            self.asteroids[i].render()

    def calculateMemoryUsage(self):
        return len(self.asteroids) * Asteroid.getMemoryUsage()

    def getAsteroidCount(self):
        return len(self.asteroids)


class WithoutFlyWeight:
    @staticmethod
    def main(args):
        ASTEROID_COUNT = 1_000_000

        print("\n TESTING WITHOUT FLYWEIGHT PATTERN")
        game = SpaceGame()

        game.spawnAsteroids(ASTEROID_COUNT)

        # Show first 5 asteroids to see the pattern
        game.renderAll()

        # Calculate and display memory usage
        totalMemory = game.calculateMemoryUsage()

        print("\n=== MEMORY USAGE ===")
        print("Total asteroids: " + str(ASTEROID_COUNT))
        print("Memory per asteroid: " + str(Asteroid.getMemoryUsage()) + " bytes")
        print("Total memory used: " + str(totalMemory) + " bytes")
        print("Memory in MB: " + str(totalMemory / (1024.0 * 1024.0)) + " MB")


if __name__ == "__main__":
    import sys
    WithoutFlyWeight.main(sys.argv[1:])
