# %% Imports
from tsp import City, GA
import matplotlib.pyplot as plt
import random

# %% Generate Cities
cities = [City(random.randint(0, 200), random.randint(0, 200)) for i in range(0, 20)]

# %% Create GA
ga = GA(cities)

# %% Evolve & Plot
for i in range(0, 500):
    ga.cycle()
plt.plot(ga.evolvement)
# print([city.__str__() for city in ga.breed(population.rank()[0], population.rank()[1])])
# print([city.__str__() for city in cities])
# print([[city.__str__() for city in route] for route in routes])
# print([route.getDistance() for route in population.rank()])
