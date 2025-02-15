import math
from mesa import Agent
from agents.trash_agent import TrashAgent
from agents.collection_station import CollectionStation

class BoatAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.status = "searching"  # Boat's current status
        self.cargo = None  # Trash being carried
        self.target = None  # Current target (trash or station)

    def step(self):
        if self.status == "searching":
            # Find trash in the vicinity
            trash = self.find_trash()
            if trash:
                self.target = trash
                self.status = "collecting"
                self.model.log_message(self, self.target, "Found trash")
                print(f"Boat {self.unique_id} found trash at {self.target.pos}")

        elif self.status == "collecting":
            if self.target is None:
                print(f"Boat {self.unique_id} has no target. Resetting to searching.")
                self.status = "searching"
                return

            # Move towards the trash
            self.move_towards(self.target.pos)
            if self.pos == self.target.pos:
                # Pick up the trash
                self.cargo = self.target
                self.model.grid.remove_agent(self.target)
                self.model.schedule.remove(self.target)
                self.status = "transporting"
                self.target = None
                print(f"Boat {self.unique_id} picked up trash at {self.cargo.pos}")

        elif self.status == "transporting":
            if self.cargo is None:
                print(f"Boat {self.unique_id} has no cargo. Resetting to searching.")
                self.status = "searching"
                return

            # Find the nearest collection station
            station = self.find_nearest_station()
            if station:
                self.target = station
                self.move_towards(self.target.pos)
                if self.pos == self.target.pos:
                    # Drop off the trash
                    self.cargo = None
                    self.status = "searching"
                    self.target = None
                    print(f"Boat {self.unique_id} dropped off trash at {station.pos}")

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
            print(f"Boat {self.unique_id} cannot move towards None target.")
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