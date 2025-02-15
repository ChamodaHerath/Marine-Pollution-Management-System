# Marine Pollution Management System

## Overview
This project is a multi-agent simulation designed to address marine pollution by automating trash collection in waterways. The system incorporates three types of agents:

- **Drones**: Identify and collect trash.
- **Boats**: Transport collected trash to collection stations.
- **Collection Stations**: Centralized locations for processing collected trash.

The simulation is built using **MESA** for agent-based modeling and **Pygame** for visualization. It demonstrates how autonomous agents can work together to clean up polluted water bodies efficiently.

## Features
- **Dynamic Trash Generation**: Trash is generated randomly during the simulation to mimic real-world pollution.
- **Agent Collaboration**: 
  - Drones search for trash and collect it.
  - Boats transport collected trash to collection stations.
- **Visualization**:
  - Real-time visualization of agents (drones, boats, trash, and collection stations) on a grid.
  - A legend on the left side explains the shapes and colors of agents.
  - A message log on the right side displays agent interactions (e.g., "Drone found trash").
- **Continuous Simulation**: The simulation runs indefinitely, dynamically generating new trash and cleaning it up.

## File Structure
The project is organized as follows:
![image](https://github.com/user-attachments/assets/7e437216-8bd0-4c90-bd6a-1e38fd277c6f)


## How It Works

### Agents:
- **Drones**: Search for trash, collect it, and return to collection stations.
- **Boats**: Transport trash from drones to collection stations.
- **Collection Stations**: Receive and process trash.
- **Trash**: Randomly generated on the grid, representing pollution.

### Simulation:
- The simulation runs in steps, with agents performing their tasks (searching, collecting, transporting) at each step.
- Trash is dynamically generated to keep the simulation running.

### Visualization:
- The grid is displayed in the center of the window.
- Agents are represented by shapes and colors:
  - **Drones**: Blue circles
  - **Boats**: Green rectangles
  - **Collection Stations**: Red triangles
  - **Trash**: Gray squares
- A legend on the left side explains the shapes and colors.
- A message log on the right side displays agent interactions.
![image](https://github.com/user-attachments/assets/f866479c-12d9-480c-87c3-c9369ff99d73)


## Requirements
To run the project, you need the following Python libraries:
- `mesa` (for agent-based modeling)
- `pygame` (for visualization)
- `pygame_gui` (for UI elements)


