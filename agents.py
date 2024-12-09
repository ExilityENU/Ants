import networkx as nx
import random

class Ant:
    """Agent navigating the graph-based environment."""
    def __init__(self, environment, nest, colony_id):
        self.environment = environment
        self.current_position = nest
        self.carrying = None
        self.colony_id = colony_id

    def find_best_resource(self):
        # Filter resources to only those in valid nodes and reachable
        reachable_resources = [
            res for res in self.environment.resources
            if res["pos"] in self.environment.graph.nodes
               and nx.has_path(self.environment.graph, self.current_position, res["pos"])
        ]
        if not reachable_resources:
            return None  # No reachable resources

        # Choose the best resource based on utility and distance
        best_resource = max(
            reachable_resources,
            key=lambda res: res["utility"] / max(1, nx.shortest_path_length(
                self.environment.graph, self.current_position, res["pos"]
            ))  # Avoid division by zero
        )
        return best_resource

    def act(self):
        # Ensure the agent's current position is valid
        if self.current_position not in self.environment.graph.nodes:
            # Move to a random valid node if the current position is invalid
            self.current_position = random.choice(list(self.environment.graph.nodes))
            return

        if self.carrying:
            # Return to the nest
            if self.environment.nest in self.environment.graph.nodes and nx.has_path(self.environment.graph,
                                                                                     self.current_position,
                                                                                     self.environment.nest):
                path = nx.shortest_path(self.environment.graph, self.current_position, self.environment.nest,
                                        weight="weight")
                if len(path) > 1:
                    self.current_position = path[1]  # Move to the next step
                if self.current_position == self.environment.nest:
                    self.carrying = None
        else:
            # Search for resources
            best_resource = self.find_best_resource()
            if best_resource:
                if self.current_position == best_resource["pos"]:
                    # Collect the resource immediately if already on it
                    self.carrying = best_resource["type"]
                    self.environment.resources.remove(best_resource)
                else:
                    # Navigate to the resource
                    path = nx.shortest_path(self.environment.graph, self.current_position, best_resource["pos"],
                                            weight="weight")
                    if len(path) > 1:
                        self.current_position = path[1]
            else:
                # Move randomly if no resources are reachable
                neighbors = list(self.environment.graph.neighbors(self.current_position))
                if neighbors:
                    self.current_position = random.choice(neighbors)



