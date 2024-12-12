import networkx as nx
import random


class Ant:
    def __init__(self, environment, nest, colony_id):
        self.environment = environment
        self.current_position = nest
        self.carrying = None
        self.colony_id = colony_id

    def move_to(self, new_position, occupied_positions):
        if new_position not in occupied_positions:
            self.current_position = new_position
            return True
        return False

    def find_best_resource(self):
        reachable_resources = [
            res for res in self.environment.resources
            if nx.has_path(self.environment.graph, self.current_position, res["pos"])
        ]
        if not reachable_resources:
            return None

        best_resource = max(
            reachable_resources,
            key=lambda res: res["utility"] / (nx.shortest_path_length(
                self.environment.graph, self.current_position, res["pos"]
            ) or 1)
        )
        return best_resource


class WorkerAnt(Ant):
    def act(self, agents, occupied_positions):
        if not self.carrying:

            best_resource = self.find_best_resource()
            if best_resource:
                path = nx.shortest_path(self.environment.graph, self.current_position, best_resource["pos"],
                                        weight="weight")
                if len(path) > 1:
                    next_position = path[1]
                    self.environment.add_pheromone([self.current_position])  # Add pheromone at current position
                    self.current_position = next_position
                if self.current_position == best_resource["pos"]:
                    self.carrying = best_resource["type"]
                    self.environment.resources.remove(best_resource)
        else:
            # Return to nest
            path = nx.shortest_path(self.environment.graph, self.current_position,
                                    self.environment.nests[self.colony_id], weight="weight")
            if len(path) > 1:
                next_position = path[1]
                self.environment.add_pheromone([self.current_position])  # Add pheromone at current position
                self.current_position = next_position
            if self.current_position == self.environment.nests[self.colony_id]:
                self.environment.colony_food_count[self.colony_id] += 1  # Log food collection
                print(
                    f"Colony {self.colony_id} collected food. Total: {self.environment.colony_food_count[self.colony_id]}")
                self.carrying = None


class SoldierAnt(Ant):
    def __init__(self, environment, nest, colony_id):
        super().__init__(environment, nest, colony_id)
        self.attack_radius = 3

    def act(self, agents, occupied_positions):
        for agent in agents:
            if agent.colony_id != self.colony_id:
                try:
                    distance = nx.shortest_path_length(
                        self.environment.graph, self.current_position, agent.current_position
                    )
                    if distance <= self.attack_radius:
                        agent.current_position = self.environment.nests[agent.colony_id]
                        return
                except nx.NetworkXNoPath:
                    continue
        neighbors = list(self.environment.graph.neighbors(self.current_position))
        if neighbors:
            self.current_position = random.choice(neighbors)


class QueenAnt(Ant):
    def act(self, agents, occupied_positions):
        self.current_position = self.environment.nests[self.colony_id]
