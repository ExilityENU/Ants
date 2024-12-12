import pygame
from environment import Environment
from agents import WorkerAnt, SoldierAnt, QueenAnt
from simulation import Simulation


def main():
    pygame.init()  # this initialises the pygame

    # all the settings below can change the map
    grid_size = 50
    num_resources = 45  # how many spawn when game is stated
    num_colonies = 3
    num_agents_per_colony = 6
    cell_size = 20

    screen = pygame.display.set_mode((grid_size * cell_size, grid_size * cell_size))
    pygame.display.set_caption("Ant-Mania")
    clock = pygame.time.Clock()

    environment = Environment(grid_size, num_resources, num_colonies=num_colonies)
    agents = []
    for colony_id, nest in enumerate(environment.nests):
        agents.append(QueenAnt(environment, nest, colony_id))
        for _ in range(num_agents_per_colony // 2):
            agents.append(WorkerAnt(environment, nest, colony_id))
        for _ in range(num_agents_per_colony // 2):
            agents.append(SoldierAnt(environment, nest, colony_id))

    simulation = Simulation(environment, agents, winning_food_count=40)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if simulation.winner is None:
            simulation.step()
            simulation.draw(screen, cell_size)
        else:
            print(f"Simulation Ended! Nest {simulation.winner} wins!")
            simulation.display_scores()  # shows food score in terminal
            running = False

        pygame.display.flip()
        clock.tick(15)

    pygame.quit()


if __name__ == "__main__":
    main()
