import random
import numpy as np
import matplotlib.pyplot as plt
from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation

# Classe per a les preses
class Prey(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.strategy = "random"
        self.captured = False

    def step(self):
        if not self.captured:
            # Moviment aleatori
            dx = random.uniform(-1, 1)
            dy = random.uniform(-1, 1)
            x, y = self.model.space.get_position(self)
            new_position = (x + dx, y + dy)
            self.model.space.move_agent(self, new_position)

# Model del món de predadors i preses
class PredatorPreyModel(Model):
    def __init__(self, width, height, num_hunters, num_preys):
        super().__init__()
        self.random = random.Random()
        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.preys = []

        for i in range(num_preys):
            prey = Prey(i, self)
            self.space.place_agent(prey, (self.random.uniform(0, width), self.random.uniform(0, height)))
            self.schedule.add(prey)
            self.preys.append(prey)

        # NOTA: podries afegir caçadors aquí si cal

    def step(self):
        self.schedule.step()

# Paràmetres de simulació
NUM_HUNTERS = 0
NUM_PREYS = 5

model = PredatorPreyModel(10, 10, NUM_HUNTERS, NUM_PREYS)

# Executar 10 passos
for i in range(10):
    model.step()

print("Simulació acabada.")
