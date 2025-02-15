import random
import math
from agents.collection_station import CollectionStation
from mesa import Agent
from agents.trash_agent import TrashAgent

class DroneAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.status = "searching"
        self.target = None

    def step(self):
        if self.status == "searching":
            # Find trash in the vicinity
            trash = self.find_trash()
            if trash:
                self.target = trash
                self.status = "collecting"
                self.model.log_message(self, self.target, "Found trash")
                print(f"Drone {self.unique_id} found trash at {self.target.pos}")
        
        elif self.status == "collecting":
            if self.target is None:
                print(f"Drone {self.unique_id} has no target. Resetting to searching.")
                self.status = "searching"
                return

            # Move towards the trash
            self.move_towards(self.target.pos)
            if self.pos == self.target.pos:
                # Collect the trash
                print(f"Drone {self.unique_id} collected trash at {self.target.pos}")
                self.model.grid.remove_agent(self.target)
                self.model.schedule.remove(self.target)
                self.status = "returning"
                self.target = None

        elif self.status == "returning":
            # Return to a collection station
            station = self.find_nearest_station()
            if station:
                self.move_towards(station.pos)
                if self.pos == station.pos:
                    print(f"Drone {self.unique_id} returned to station at {station.pos}")
                    self.status = "searching"

    def find_trash(self):
        # Find trash in the grid
        trash = [agent for agent in self.model.schedule.agents if isinstance(agent, TrashAgent)]
        if trash:
            return self.find_closest(trash)
        return None

    def find_nearest_station(self):
        # Find the nearest collection station
        stations = [agent for agent in self.model.schedule.agents if isinstance(agent, CollectionStation)]
        if stations:
            return self.find_closest(stations)
        return None

    def find_closest(self, agents):
        # Find the closest agent
        return min(agents, key=lambda agent: math.sqrt(
            (self.pos[0] - agent.pos[0])**2 + (self.pos[1] - agent.pos[1])**2
        ))

    def move_towards(self, target_pos):
        # Ensure target_pos is not None
        if target_pos is None:
            print(f"Drone {self.unique_id} cannot move towards None target.")
            return

        # Move towards the target position
        dx = target_pos[0] - self.pos[0]
        dy = target_pos[1] - self.pos[1]
        
        if abs(dx) > abs(dy):
            new_x = self.pos[0] + (1 if dx > 0 else -1)
            new_y = self.pos[1]
        else:
            new_x = self.pos[0]
            new_y = self.pos[1] + (1 if dy > 0 else -1)
        
        new_x = max(0, min(new_x, self.model.grid.width - 1))
        new_y = max(0, min(new_y, self.model.grid.height - 1))
        
        self.model.grid.move_agent(self, (new_x, new_y))