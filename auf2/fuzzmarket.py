# %% Imports
from random import randint


# %% Class Definition
class FuzzySet():
    def __init__(self, borders):
        self.borders = borders

    def getMatch(self, input):
        for i in range(0, len(self.borders)):
            lower = self.borders[i]
            try:
                upper = self.borders[i + 1]
                if input >= lower[0] and input < upper[0]:
                    return ((upper[1] - lower[1]) / (upper[0] - lower[0]))*(input - lower[0]) + lower[1]
            except IndexError:
                return lower[1]


class Supermarket():
    def __init__(self, noOfProducts=5, maxCapProduct=50, random=True, stdFuzzySet=True):
        self.noOfProducts = noOfProducts
        self.maxCapProduct = maxCapProduct
        if stdFuzzySet:
            self.demand = [FuzzySet([[0, 1], [15, 1], [20, 0]]),
                           FuzzySet([[15, 0], [25, 1], [35, 1], [40, 0]]),
                           FuzzySet([[35, 0], [40, 1]])]
            self.supply = [FuzzySet([[0, 1], [10, 1], [15, 0]]),
                           FuzzySet([[5, 0], [15, 1], [20, 1], [35, 0]]),
                           FuzzySet([[20, 0], [40, 1]])]
            self.capacity = [FuzzySet([[0, 1], [self.noOfProducts / 3 * maxCapProduct, 1], [self.noOfProducts / 3 * 2 * maxCapProduct, 0]]),
                             FuzzySet([[self.noOfProducts / 3 * maxCapProduct, 0], [self.noOfProducts / 3 * 2 * maxCapProduct, 1], [self.noOfProducts / 3 * 3 * maxCapProduct, 0]]),
                             FuzzySet([[self.noOfProducts / 3 * 2 * maxCapProduct, 0], [self.noOfProducts * maxCapProduct, 1]])]
        if random:
            self.setProducts()

    def setProducts(self, products=None, random=True):
        self.products = []
        if random:
            for i in range(0, self.noOfProducts):
                self.products.append([randint(0, self.maxCapProduct), randint(0, self.maxCapProduct)])
        if products:
            self.products = products
        self.storage = sum([x[0] for x in self.products])
        self.capacity_value = [[self.capacity[0].getMatch(self.storage), "low"], [self.capacity[1].getMatch(self.storage), "middle"], [self.capacity[2].getMatch(self.storage), "high"]]
        self.capacity_value = self.capacity_value[[x[0] for x in self.capacity_value].index(max([x[0] for x in self.capacity_value]))]
        print("Storage:\t{}\nCapacity:\t{}\nProducts:\t{}".format(self.storage, self.capacity_value, self.products))

    def setFuzzySet(self, type, set):
        if type == 'demand':
            self.demand = set
        elif type == 'supply':
            self.supply = set
        elif type == 'capacity':
            self.capacity = set

    def getRecommendation(self, product):
        supply_value = [[self.supply[0].getMatch(product[0]), "low"], [self.supply[1].getMatch(product[0]), "middle"], [self.supply[2].getMatch(product[0]), "high"]]
        demand_value = [[self.demand[0].getMatch(product[1]), "low"], [self.demand[1].getMatch(product[1]), "middle"], [self.demand[2].getMatch(product[1]), "high"]]
        supply_value = supply_value[[x[0] for x in supply_value].index(max([x[0] for x in supply_value]))]
        demand_value = demand_value[[x[0] for x in demand_value].index(max([x[0] for x in demand_value]))]
        maxi = min(supply_value[0], demand_value[0])

        print("Supply:\t{}\nDemand:\t{}\nMax:\t{}\nProduct:\t{}\nMax Cap:\t{}\n\n".format(supply_value, demand_value, maxi, product, self.maxCapProduct))

        if demand_value[1] == "high":
            if supply_value[1] == "high":
                return [0, "low"]
            elif self.capacity_value[1] == "middle" or self.capacity_value[1] == "low":
                if supply_value[1] == "low":
                    return [round(maxi * (self.maxCapProduct - product[0]), 0), "high"]
                elif supply_value[1] == "middle":
                    return [round(maxi * .5 * (self.maxCapProduct - product[0]), 0), "middle"]
            elif self.capacity_value[1] == "high":
                return [round(maxi * .4 * (self.maxCapProduct - product[0]), 0), "middle"]
        elif demand_value[1] == "middle":
            if supply_value[1] == "middle" or supply_value[1] == "high":
                return [0, "low"]
            elif self.capacity_value[1] == "middle" or self.capacity_value[1] == "low":
                return [round(maxi * (self.maxCapProduct - product[0]), 0), "middle"]
            elif self.capacity_value[1] == "high":
                return [round(maxi * .6 * (self.maxCapProduct - product[0]), 0), "low"]
        elif demand_value[1] == "low":
            return [0, "low"]

    def getRecommendations(self):
        result = {}
        i = 65
        for p in self.products:
            result['Product ' + chr(i)] = self.getRecommendation(p)
            i += 1
        return result
