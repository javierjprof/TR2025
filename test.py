from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.animation import FuncAnimation

# Nombre de caçadors i preses (variables modificables)
NUM_HUNTERS = 2
NUM_PREYS = 10
CAPTURE_DISTANCE = 0.5  # Distància a què es considera capturada la presa

# Classe per representar la presa
class Prey(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.strategy = "random"  # Inicialment totes les preses tenen estratègia aleatòria
        self.captured = False     # Estat de captura
    
    def move(self):
        if not self.captured:  # Només es mou si no està capturada
            dx, dy = np.random.uniform(-1, 1), np.random.uniform(-1, 1)
            new_x = min(max(self.pos[0] + dx, 0), self.model.space.width)
            new_y = min(max(self.pos[1] + dy, 0), self.model.space.height)
            self.model.space.move_agent(self, (new_x, new_y))
    
    def step(self):
        self.move()

# Classe per representar el caçador
class Hunter(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.strategy = "direct"  # El caçador segueix una estratègia directa
    
    def move(self):
        # Només considerar preses no capturades
        active_preys = [p for p in self.model.preys if not p.captured]
        
        if active_preys:
            prey = min(active_preys, key=lambda p: np.linalg.norm(np.array(self.pos) - np.array(p.pos)))
            dx, dy = np.sign(prey.pos[0] - self.pos[0]), np.sign(prey.pos[1] - self.pos[1])
            new_x = min(max(self.pos[0] + dx, 0), self.model.space.width)
            new_y = min(max(self.pos[1] + dy, 0), self.model.space.height)
            self.model.space.move_agent(self, (new_x, new_y))
            
            # Verificar si va capturar la presa
            distance = np.linalg.norm(np.array(self.pos) - np.array(prey.pos))
            if distance < CAPTURE_DISTANCE:
                prey.captured = True
    
    def step(self):
        self.move()

# Classe per al model de simulació
class PredatorPreyModel(Model):
    def __init__(self, width, height, num_hunters, num_preys):
        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.preys = []
        self.hunters = []
        
        for i in range(num_preys):
            prey = Prey(i, self)
            self.space.place_agent(prey, (np.random.uniform(0, width), np.random.uniform(0, height)))
            self.schedule.add(prey)
            self.preys.append(prey)
        
        for i in range(num_hunters):
            hunter = Hunter(i + num_preys, self)
            self.space.place_agent(hunter, (np.random.uniform(0, width), np.random.uniform(0, height)))
            self.schedule.add(hunter)
            self.hunters.append(hunter)
    
    def step(self):
        self.schedule.step()

# Executar la simulació amb 1 caçador i 2 preses
model = PredatorPreyModel(10, 10, NUM_HUNTERS, NUM_PREYS)

# Configuració de l´animació
def update(frame):
    model.step()
    plt.clf()
    
    # Dibuixar preses
    for prey in model.preys:
        if prey.captured:
            plt.scatter(prey.pos[0], prey.pos[1], color='black', label='Presa capturada' if frame == 0 else "")
        else:
            plt.scatter(prey.pos[0], prey.pos[1], color='blue', label='Presa' if frame == 0 else "")
    
    # Dibuixar caçadors
    for hunter in model.hunters:
        plt.scatter(hunter.pos[0], hunter.pos[1], color='red', label='Cazador' if frame == 0 else "")
    
    plt.legend()
    plt.xlim(0, model.space.width)
    plt.ylim(0, model.space.height)
    plt.title(f"Paso {frame}")

fig = plt.figure(figsize=(6,6))
ani = FuncAnimation(fig, update, frames=50, interval=200)  # Augmentar els frames per a més durada
plt.show()