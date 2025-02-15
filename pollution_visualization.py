from agents.boat_agent import BoatAgent
from agents.collection_station import CollectionStation
from agents.drone_agent import DroneAgent
from agents.trash_agent import TrashAgent
import pygame
from mesa.visualization.ModularVisualization import VisualizationElement

class PollutionVisualization(VisualizationElement):
    def __init__(self, grid_width, grid_height, canvas_width, canvas_height):
        super().__init__()
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.cell_width = 30  # Fixed cell width for better visualization
        self.cell_height = 30  # Fixed cell height for better visualization

        # Calculate grid position to center it
        self.grid_offset_x = (canvas_width - (grid_width * self.cell_width)) // 2
        self.grid_offset_y = (canvas_height - (grid_height * self.cell_height)) // 2

        pygame.init()
        self.screen = pygame.display.set_mode((canvas_width, canvas_height))
        pygame.display.set_caption("Marine Pollution Management System")

        # Font for text
        self.font = pygame.font.Font(None, 24)

    def render(self, model):
        # Clear the screen
        self.screen.fill((255, 255, 255))  # White background

        # Draw the grid
        self.draw_grid()

        # Draw agents
        for agent in model.schedule.agents:
            self.draw_agent(agent)

        # Draw legend on the left side
        self.draw_legend()

        # Draw message log on the right side
        self.draw_message_log(model.message_history)

        # Update the display
        pygame.display.flip()

    def draw_grid(self):
        # Draw grid lines
        for x in range(self.grid_width + 1):
            pygame.draw.line(
                self.screen,
                (200, 200, 200),  # Light gray
                (self.grid_offset_x + x * self.cell_width, self.grid_offset_y),
                (self.grid_offset_x + x * self.cell_width, self.grid_offset_y + self.grid_height * self.cell_height),
            )
        for y in range(self.grid_height + 1):
            pygame.draw.line(
                self.screen,
                (200, 200, 200),  # Light gray
                (self.grid_offset_x, self.grid_offset_y + y * self.cell_height),
                (self.grid_offset_x + self.grid_width * self.cell_width, self.grid_offset_y + y * self.cell_height),
            )

    def draw_agent(self, agent):
        x, y = agent.pos
        screen_x = self.grid_offset_x + x * self.cell_width
        screen_y = self.grid_offset_y + y * self.cell_height

        if isinstance(agent, DroneAgent):
            # Draw drone as a blue circle
            pygame.draw.circle(self.screen, (0, 0, 255), (screen_x + self.cell_width // 2, screen_y + self.cell_height // 2), self.cell_width // 3)
        elif isinstance(agent, BoatAgent):
            # Draw boat as a green rectangle
            pygame.draw.rect(self.screen, (0, 255, 0), (screen_x, screen_y, self.cell_width, self.cell_height))
        elif isinstance(agent, CollectionStation):
            # Draw station as a red triangle
            pygame.draw.polygon(self.screen, (255, 0, 0), [
                (screen_x + self.cell_width // 2, screen_y),
                (screen_x, screen_y + self.cell_height),
                (screen_x + self.cell_width, screen_y + self.cell_height),
            ])
        elif isinstance(agent, TrashAgent):
            # Draw trash as a gray square
            pygame.draw.rect(self.screen, (128, 128, 128), (screen_x, screen_y, self.cell_width, self.cell_height))

    def draw_legend(self):
        # Draw legend on the left side
        legend_x = 20
        legend_y = 20
        self.draw_legend_item("Drone", (0, 0, 255), legend_x, legend_y)  # Blue circle
        self.draw_legend_item("Boat", (0, 255, 0), legend_x, legend_y + 40)  # Green rectangle
        self.draw_legend_item("Station", (255, 0, 0), legend_x, legend_y + 80)  # Red triangle
        self.draw_legend_item("Trash", (128, 128, 128), legend_x, legend_y + 120)  # Gray square

    def draw_legend_item(self, text, color, x, y):
        # Draw a shape and text for the legend
        if text == "Drone":
            pygame.draw.circle(self.screen, color, (x + 15, y + 15), 10)
        elif text == "Boat":
            pygame.draw.rect(self.screen, color, (x, y, 30, 30))
        elif text == "Station":
            pygame.draw.polygon(self.screen, color, [
                (x + 15, y),
                (x, y + 30),
                (x + 30, y + 30),
            ])
        elif text == "Trash":
            pygame.draw.rect(self.screen, color, (x, y, 30, 30))
        
        # Draw text
        text_surface = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, (x + 40, y + 10))

    def draw_message_log(self, message_history):
        # Draw message log on the right side
        log_x = self.grid_offset_x + self.grid_width * self.cell_width + 20
        log_y = 20
        max_lines = 20  # Maximum number of messages to display

        # Display the most recent messages
        for i, msg in enumerate(reversed(message_history[-max_lines:])):
            text = f"T{msg['time']}: {msg['sender']} → {msg['receiver']}: {msg['type']}"
            text_surface = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (log_x, log_y + i * 20))