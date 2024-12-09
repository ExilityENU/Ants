import pygame
from environment import Environment
from agents import Ant
from simulation import Simulation


def main():
    pygame.init()
    grid_size = 50  # Larger map
    num_resources = 45
    num_agents = 10
    respawn_count = 5
    cell_size = 20  # Adjust for larger grid

    screen = pygame.display.set_mode((grid_size * cell_size, grid_size * cell_size))
    pygame.display.set_caption("2d ant simulation")
    clock = pygame.time.Clock()

    simulation = Simulation(
        grid_size=grid_size,
        num_resources=num_resources,
        num_agents=num_agents,
        environment_cls=lambda g, r: Environment(g, r, respawn_count),
        agent_cls=Ant
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        simulation.step()
        simulation.draw(screen, cell_size)
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
