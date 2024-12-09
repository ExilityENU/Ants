import pygame

class Simulation:
    """Manages the simulation loop and visualization."""
    def __init__(self, grid_size, num_resources, num_agents, environment_cls, agent_cls):
        # Initialize the environment
        self.environment = environment_cls(grid_size, num_resources)

        # Initialize all agents at the nest
        self.agents = [
            agent_cls(self.environment, self.environment.nest, colony_id=0)
            for _ in range(num_agents)
        ]

    def step(self):
        # Perform actions for all agents
        for agent in self.agents:
            agent.act()

        # Decay pheromones and respawn resources
        self.environment.decay_pheromones()
        self.environment.respawn_resources()

    def draw(self, screen, cell_size):
        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw terrain, resources, and agents
        for (x, y), terrain in self.environment.terrain.items():
            color = (200, 255, 200)  # Default grass color
            if terrain == "water":
                color = (0, 0, 255)
            elif terrain == "rock":
                color = (150, 150, 150)
            pygame.draw.rect(screen, color, (y * cell_size, x * cell_size, cell_size, cell_size))

        # Draw resources
        for resource in self.environment.resources:
            pygame.draw.circle(screen, (25,175, 90), (resource["pos"][1] * cell_size + cell_size // 2, resource["pos"][0] * cell_size + cell_size // 2), 5)

        # Draw nest
        pygame.draw.circle(screen, (120, 45, 13), (self.environment.nest[1] * cell_size + cell_size // 2, self.environment.nest[0] * cell_size + cell_size // 2), 10)
        # Draw agents
        for agent in self.agents:
            pygame.draw.circle(screen, (255, 0, 0), (agent.current_position[1] * cell_size + cell_size // 2, agent.current_position[0] * cell_size + cell_size // 2), 5)
