# %% Imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors


# %% Class Definition
class GoL:
    def __init__(self, size, reproduction_prey, food, predator, reproduction_predator, predator_death):
        """
            1   2   3
            4   X   5
            6   7   8
        """
        self.size = size
        self.grid = np.zeros((size, size, 3), dtype=int)
        self.reproduction_prey = reproduction_prey
        self.food = food
        self.reproduction_predator = reproduction_predator
        self.predator = predator
        self.predator_death = predator_death
        self.species = ["predator", "prey"]
        self.dict = {
            1: (-1, -1),
            2: (-1, 0),
            3: (-1, 1),
            4: (0, -1),
            5: (0, 1),
            6: (1, -1),
            7: (1, 0),
            8: (1, 1)
        }

    def cycle(self):
        for (j, i), type in np.ndenumerate([[x[0] for x in y] for y in self.grid]):
            self.think(origin=(j, i))
        for (j, i), type in np.ndenumerate([[x[0] for x in y] for y in self.grid]):
            self.grid[j][i][2] = 0

    def addEntity(self, type="prey", origin=None):
        if origin:
            y, x = origin
        else:
            y, x = np.random.randint(self.size, size=2)
            while not self.grid[y][x][0] == 0 or np.count_nonzero([[x[0] for x in y] for y in self.grid]) == self.getGridSize():
                y, x = np.random.randint(self.size, size=2)
        if type == "prey":
            self.grid[y][x] = [1, 1, 0]
        elif type == "predator":
            self.grid[y][x] = [2, self.predator, 0]

    def randomEntity(self, chances):
        return np.random.choice(self.species, p=chances)

    def move(self, direction, origin):
        y, x = origin
        y2 = self.wrap(y + self.dict.get(direction)[0])
        x2 = self.wrap(x + self.dict.get(direction)[1])
        source = self.grid[y][x]
        target = self.grid[y2][x2]
        self.grid[y2][x2] = source
        self.grid[y][x] = [0, 0, 0]
        return target

    def checkNeighbours(self, origin, state=0):
        y, x = origin
        result = []
        for d in self.dict.keys():
            y2, x2 = self.wrap(y + self.dict.get(d)[0]), self.wrap(x + self.dict.get(d)[1])
            if self.grid[y2][x2][0] == state:
                result.append(d)
        return result

    def think(self, origin):
        cell = self.grid[origin[0]][origin[1]]
        if cell[0] == 1 and cell[2] == 0:
            self.grid[origin[0]][origin[1]][2] = 1
            try:
                d = np.random.choice(self.checkNeighbours(origin=origin))
                o = self.wrap(origin[0] + self.dict.get(d)[0]), self.wrap(origin[1] + self.dict.get(d)[1])
                if cell[1] >= self.reproduction_prey:
                    self.addEntity(origin=o)
                    self.grid[origin[0]][origin[1]][1] //= 2
                else:
                    self.grid[origin[0]][origin[1]][1] += 1
                    self.move(direction=d, origin=origin)
            except ValueError:
                pass
        elif cell[0] == 2 and cell[2] == 0 and cell[1] <= 1:
            self.grid[origin[0]][origin[1]] = [0, 0, 0]
        elif cell[0] == 2 and cell[2] == 0:
            self.grid[origin[0]][origin[1]][2] = 1
            try:
                d = np.random.choice(self.checkNeighbours(origin=origin, state=1))
                o = self.wrap(origin[0] + self.dict.get(d)[0]), self.wrap(origin[1] + self.dict.get(d)[1])
                if cell[1] >= self.reproduction_predator:
                    self.addEntity(origin=o, type="predator")
                    self.grid[origin[0]][origin[1]][1] //= 2
                else:
                    self.grid[origin[0]][origin[1]][1] += self.food
                    self.grid[origin[0]][origin[1]][1] -= 1
                    self.move(direction=d, origin=origin)
            except ValueError:
                d = np.random.choice(self.checkNeighbours(origin=origin, state=0))
                o = self.wrap(origin[0] + self.dict.get(d)[0]), self.wrap(origin[1] + self.dict.get(d)[1])
                if cell[1] >= self.reproduction_predator:
                    self.addEntity(origin=o, type="predator")
                    self.grid[origin[0]][origin[1]][1] //= 2
                elif np.random.choice([0, 1], p=[1-self.predator_death, self.predator_death]) == 1:
                    self.grid[origin[0]][origin[1]] = [0, 0, 0]
                else:
                    self.grid[origin[0]][origin[1]][1] -= 1
                    self.move(direction=d, origin=origin)

    def wrap(self, x):
            if x == self.size:
                return 0
            elif x < 0:
                return self.size - 1
            else:
                return x

    def plotGrid(self):
        cmap = colors.ListedColormap(['#ffffff', '#00e600', '#e60000'])
        boundaries = [0, 1, 2, 3]
        norm = colors.BoundaryNorm(boundaries, cmap.N, clip=True)
        plt.imshow([[x[0] for x in y] for y in self.grid], cmap=cmap, norm=norm)
        for (j, i), label in np.ndenumerate([[x[1] for x in y] for y in self.grid]):
            plt.text(i, j, label, ha='center', va='center')
        plt.show()

    def getGridSize(self):
        return self.size * self.size
