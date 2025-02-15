from models.pollution_model import PollutionModel
from visualization.pollution_visualization import PollutionVisualization
import pygame

def main():
    # Simulation parameters
    width, height = 20, 20
    num_drones = 3
    num_boats = 2
    num_stations = 4
    num_trash = 25 

    # Create the model
    model = PollutionModel(width, height, num_drones, num_boats, num_stations, num_trash)

    # Create the visualization
    visualization = PollutionVisualization(width, height, 1500, 700)

     # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Run the simulation
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Step the model
        model.step()

        # Render the visualization
        visualization.render(model)

        # Add a delay to slow down the simulation
        pygame.time.delay(200)  # 200ms delay (adjust as needed)

        # Limit the frame rate
        clock.tick(10)  # 10 FPS (adjust as needed)
    pygame.quit()    

if __name__ == "__main__":
    main()