from mesa import Agent # type: ignore

class CollectionStation(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.capacity = 100
        self.current_load = 0

    def step(self):
        # Process waste if there is any
        if self.current_load > 0:
            self.current_load -= 1