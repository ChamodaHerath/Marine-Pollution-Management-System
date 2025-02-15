from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents.drone_agent import DroneAgent
from agents.boat_agent import BoatAgent
from agents.collection_station import CollectionStation
from agents.trash_agent import TrashAgent
import random

class PollutionModel(Model):
    def __init__(self, width, height, num_drones, num_boats, num_stations, num_trash):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.num_trash = num_trash
        self.width = width
        self.height = height
        self.message_history = []  # Initialize message history

        # Create drones
        for i in range(num_drones):
            drone = DroneAgent(i, self)
            self.schedule.add(drone)
            self.grid.place_agent(drone, self.random_position())

        # Create boats
        for i in range(num_boats):
            boat = BoatAgent(i + num_drones, self)
            self.schedule.add(boat)
            self.grid.place_agent(boat, self.random_position())

        # Create collection stations
        for i in range(num_stations):
            station = CollectionStation(i + num_drones + num_boats, self)
            self.schedule.add(station)
            self.grid.place_agent(station, self.random_position())

        # Create initial trash
        for i in range(num_trash):
            trash = TrashAgent(i + num_drones + num_boats + num_stations, self)
            self.schedule.add(trash)
            self.grid.place_agent(trash, self.random_position())

    def random_position(self):
        # Generate a random position on the grid
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        return (x, y)

    def step(self):
        # Generate new trash dynamically
        if random.random() < 0.1:  # 10% chance to generate new trash
            new_trash = TrashAgent(len(self.schedule.agents), self)
            self.schedule.add(new_trash)
            self.grid.place_agent(new_trash, self.random_position())

        # Step the schedule
        self.schedule.step()

    def log_message(self, sender, receiver, message_type):
        # Log a message
        self.message_history.append({
            'time': self.schedule.time,
            'sender': sender.__class__.__name__,
            'receiver': receiver.__class__.__name__,
            'type': message_type,
        })