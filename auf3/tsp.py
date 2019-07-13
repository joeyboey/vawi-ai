# %% Imports
import random


# %% Class Definitions
class City:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def getDistance(self, city):
        return ((abs(self.x - city.x) ** 2) + (abs(self.y - city.y) ** 2)) ** .5

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


class Route:
    def __init__(self, route):
        self.route = route

    def getDistance(self):
        distance, route = 0, self.route + [self.route[0]]
        for pair in zip(route, route[1:]):
            distance += pair[0].getDistance(pair[1])
        return distance


class Population:
    def __init__(self, routes):
        self.routes = routes

    def rank(self):
        return sorted(self.routes, key=Route.getDistance)


class GA:
    def __init__(self, cities, size=200, elites=.2, mutation=.005):
        self.population = Population([Route(route) for route in [random.sample(cities, len(cities)) for i in range(0, size)]]).rank()
        self.size = size
        self.elites = int(elites * size)
        self.mutation = mutation
        self.evolvement = []

    def select(self, population):
        return population[:self.elites] + [r for r in population[self.elites:] if population[0].getDistance() / r.getDistance() >= random.random()]

    def breed(self, mum, dad):
        a, b = random.randint(0, len(mum.route)), random.randint(0, len(mum.route))
        m = mum.route[min(a, b):max(a, b)]
        return Route(m + [c for c in dad.route if c not in m])

    def breedAll(self, selection):
        return selection[:self.elites] + [self.breed(mum, dad) for mum, dad in [random.sample(selection[self.elites:], 2) for i in range(0, self.size - self.elites)]]

    def mutate(self, route):
        a, b = random.sample(route, 2)
        ia, ib = route.index(a), route.index(b)
        if self.mutation >= random.random():
            route[ia], route[ib] = route[ib], route[ia]
        return route

    def cycle(self):
        self.population = Population([Route(self.mutate(route.route)) for route in self.breedAll(self.select(self.population))]).rank()
        self.evolvement.append([self.population[0].getDistance(), sum([r.getDistance() for r in self.population]) / len(self.population)])
