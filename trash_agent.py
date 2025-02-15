from mesa import Agent # type: ignore

class TrashAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)