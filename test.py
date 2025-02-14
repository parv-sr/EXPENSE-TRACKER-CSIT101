import mesa
from mesa import Agent, Model
from mesa import time
from time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid

import random
import numpy as np
import matplotlib.pyplot as plt

class Agent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.knowledge = 1


    def spread_news(self):
        if self.knowledge == 0:
            return
        neighbours = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True)
        neigh_agents = [a for n in neighbours for a in self.model.grid.get_cell_list_contents(n.pos)]

        for a in neigh_agents:
            if random.random()<0.3:
                a.knowledge = 1

    
    def step(self):
        self.move()
        self.spread_news()
        
    def compute_informed(model):
        return sum([1 for a in model.schedule.agents if a.knowledge == 1])
    


class news_model(model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        for i in range(self.num_agents):
            a = Agent(i, self)
            self.schedule.add(a)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            agent_reporters = {"knowledge": "knowledge"}
            model_reporters = {"Informed": compute_informed}
        )
