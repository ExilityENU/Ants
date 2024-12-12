import pygame


from agents import WorkerAnt, SoldierAnt


class Simulation:
    def __init__(self, environment, agents, winning_food_count=40):
        self.environment = environment
        self.agents = agents
        self.winning_food_count = winning_food_count
        self.winner = None
        self.occupied_positions = set()  # Track occupied tiles

    def step(self):
        if self.winner is None:
            self.occupied_positions.clear()  # Reset occupied positions at the start of each step
            for agent in self.agents:
                self.occupied_positions.add(agent.current_position)  # Mark current position as occupied
            for agent in self.agents:
                agent.act(self.agents, self.occupied_positions)
            self.environment.decay_pheromones()
            self.check_winner()

    def check_winner(self):
        for colony_id, food_count in self.environment.colony_food_count.items():
            if food_count >= self.winning_food_count:
                self.winner = colony_id
                print(f"Colony {colony_id} wins with {food_count} food collected!")

    def display_scores(self):
        print("Final Scores:")
        for colony_id, food_count in self.environment.colony_food_count.items():
            print(f"Colony {colony_id}: {food_count} food collected")

    def draw(self, screen, cell_size):
        screen.fill((255, 255, 255))
        pass
        # Draw terrain
        for (x, y), terrain in self.environment.terrain.items():
            color = (200, 255, 200) if terrain == "grass" else (0, 0, 255) if terrain == "water" else (150, 150, 150)
            pygame.draw.rect(screen, color, (y * cell_size, x * cell_size, cell_size, cell_size))

        # Draw resources
        for resource in self.environment.resources:
            pygame.draw.circle(screen, (0, 255, 0), (
                resource["pos"][1] * cell_size + cell_size // 2, resource["pos"][0] * cell_size + cell_size // 2), 5)

        # Draw nests
        for nest in self.environment.nests:
            pygame.draw.circle(screen, (255, 165, 0),
                               (nest[1] * cell_size + cell_size // 2, nest[0] * cell_size + cell_size // 2), 10)

        # Draw agents
        for agent in self.agents:
            color = (255, 2, 255) if isinstance(agent, WorkerAnt) else (255, 0, 0) if isinstance(agent,
                                                                                                 SoldierAnt) else (
                0, 0, 255)
            pygame.draw.circle(screen, color, (agent.current_position[1] * cell_size + cell_size // 2,
                                               agent.current_position[0] * cell_size + cell_size // 2), 5)
