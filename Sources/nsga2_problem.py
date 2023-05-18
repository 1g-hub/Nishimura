from nsga2_individual import Individual
import random
import numpy as np


class Problem:

    def __init__(self, objectives, num_of_variables, variables_range, expand=True, same_range=False):
        self.num_of_objectives = len(objectives)
        self.num_of_variables = num_of_variables
        self.objectives = objectives
        self.expand = expand
        self.variables_range = []
        if same_range:
            for _ in range(num_of_variables):
                self.variables_range.append(variables_range[0])
        else:
            self.variables_range = variables_range


    def generate_individual(self):
        individual = Individual()

        deck = []

        for _ in range(self.num_of_variables):
            deck.append(random.randint(self.variables_range[0][0], self.variables_range[0][1]))


        individual.features = deck
        #print(individual.features)


        #print(individual.features)
        return individual

    
    def calculate_objectives(self, individual):
        if self.expand:
            individual.objectives = [f(individual.features) for f in self.objectives]
        else:
            individual.objectives = [f(individual.features) for f in self.objectives]