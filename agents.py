import networkx as nx
import random


class Ant:
    # this is the default class for all ants, shared functions lay here
    def __init__(self, environment, nest, colony_id):
        self.environment = environment
        self.current_position = nest
        self.carrying = None
        self.colony_id = colony_id

    def move_to(self, new_position, occupied_positions):
        # to stop ants from piling up on one tile, so this ensures they only go on an empty tile
        if new_position not in occupied_positions:
            self.current_position = new_position
            return True
        return False

    def find_best_resource(self):
        # finds the best resource based on utility and path cost
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


class SoldierAnt(Ant):
    def act(self, agents, occupied_positions):
        # find nearby enemy soldier ants
        for agent in agents:
            if isinstance(agent, SoldierAnt) and agent.colony_id != self.colony_id:
                try:
                    distance = nx.shortest_path_length(self.environment.graph, self.current_position,
                                                       agent.current_position)
                    if distance == 4:  # engage in combat if distance is 4 tiles
                        self.fight(agent)
                        return  # stop further actions this step
                except nx.NetworkXNoPath:
                    continue

        # move randomly if no enemies nearby
        neighbors = list(self.environment.graph.neighbors(self.current_position))
        if neighbors:
            next_position = random.choice(neighbors)
            if self.move_to(next_position, occupied_positions):
                occupied_positions.add(next_position)

    def fight(self, enemy):
        # logic for all the fighting between the ants
        print(f"Soldier from Nest {self.colony_id + 1} is fighting Soldier from Nest {enemy.colony_id + 1}")
        if random.random() > 0.5:  # 50% chance to win
            print(f"Soldier from Nest {enemy.colony_id + 1} defeated!")
            enemy.respawn()
        else:
            print(f"Soldier from Nest {self.colony_id + 1} defeated!")
            self.respawn()

    def respawn(self):

        self.current_position = self.environment.nests[self.colony_id]
        print(f"Soldier from Nest {self.colony_id + 1} has respawned at the nest.")


class QueenAnt(Ant):  # stays at nest during the sim, no movements no actions
    def act(self, agents, occupied_positions):
        self.current_position = self.environment.nests[self.colony_id]


class WorkerAnt(Ant):  # below has code for the worker ants to drop pheromone trail, pathfinding, and food collection
    def act(self, agents, occupied_positions):
        if not self.carrying:

            best_resource = self.find_best_resource()
            if best_resource:
                path = nx.shortest_path(self.environment.graph, self.current_position, best_resource["pos"],
                                        weight="weight")
                if len(path) > 1:
                    next_position = path[1]
                    self.environment.add_pheromone([self.current_position])  # add pheromone at current position
                    self.current_position = next_position
                    self.move_to(next_position, occupied_positions)  # stops ants being on the same tile
                if self.current_position == best_resource["pos"]:
                    self.carrying = best_resource["type"]
                    self.environment.resources.remove(best_resource)
        else:
            # return to nest
            path = nx.shortest_path(self.environment.graph, self.current_position,
                                    self.environment.nests[self.colony_id], weight="weight")
            if len(path) > 1:
                next_position = path[1]
                self.environment.add_pheromone([self.current_position])
                self.current_position = next_position
                self.move_to(next_position, occupied_positions)
            if self.current_position == self.environment.nests[self.colony_id]:
                self.environment.colony_food_count[self.colony_id] += 1
                print(
                    f"Nest {self.colony_id + 1} collected food. Total: {self.environment.colony_food_count[self.colony_id]}")
                self.carrying = None
