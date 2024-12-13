import networkx as nx
import random
import time


class Environment:
    def __init__(self, grid_size, num_resources, respawn_count=1, num_colonies=2):
        # manages all the interaction between the agents, resources and the grid-based graph world
        self.graph = nx.Graph()
        self.grid_size = grid_size
        self.nests = []
        self.resources = []
        self.respawn_timer = time.time()
        self.respawn_count = respawn_count
        self.terrain = {}
        self.pheromone_grid = {}
        self.colony_food_count = {i: 0 for i in range(num_colonies)}  # track food count for each colony
        self._initialize_graph()
        self._generate_terrain()
        self._place_nests(num_colonies)
        self._place_resources(num_resources)

    def _initialize_graph(self):
        directions = [
            (1, 0), (0, 1), (-1, 0), (0, -1),  # cardinal directions
            (1, 1), (-1, -1), (1, -1), (-1, 1)
            # diagonal directions, both movement options allow the ant to be more realistic
        ]
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                self.graph.add_node((x, y))
                for dx, dy in directions:
                    next_x, next_y = x + dx, y + dy
                    if 0 <= next_x < self.grid_size and 0 <= next_y < self.grid_size:
                        self.graph.add_edge((x, y), (next_x, next_y), weight=1.0)

    def _generate_terrain(self):  # randomly generate terrain
        terrain_weights = {"grass": 0.60, "rock": 0.30, "water": 0.10}  # % for grass, rocks, water
        terrain_types = list(terrain_weights.keys())
        terrain_probabilities = list(terrain_weights.values())

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                terrain = random.choices(terrain_types, weights=terrain_probabilities, k=1)[0]
                self.terrain[(x, y)] = terrain
                if terrain == "water":
                    self.graph.remove_node((x, y))
                elif terrain == "rock":
                    for neighbor in list(self.graph.neighbors((x, y))):
                        if self.graph.has_edge((x, y), neighbor):
                            self.graph[(x, y)][neighbor]["weight"] = 2.0

    def _place_nests(self, num_colonies):  # randomly spawn nest in the map
        for _ in range(num_colonies):
            while True:
                x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
                if self.terrain.get((x, y)) == "grass" and (x, y) not in self.nests:
                    self.nests.append((x, y))
                    break

    def _place_resources(self, num_resources):  # randomly spawn first set of resources
        for _ in range(num_resources):
            self.add_resource()

    # all print functions here are commented out as they are used for testing

    def add_resource(self):  # new resource to a random valid grid location
        while True:
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if (x, y) not in self.nests and (x, y) in self.graph.nodes:
                resource_type = random.choice(["food", "water", "energy"])
                utility = {"food": 10, "water": 5, "energy": 10}[resource_type]
                self.resources.append({"pos": (x, y), "type": resource_type, "utility": utility})
                # print(f"resource added: {resource_type} at ({x}, {y})")
                break

    def add_pheromone(self, path):
        current_time = time.time()
        for position in path:
            self.pheromone_grid[position] = current_time
            # print(f"pheromone added at {position} at time {current_time}")

    def decay_pheromones(self):
        current_time = time.time()
        for position in list(self.pheromone_grid.keys()):
            if current_time - self.pheromone_grid[position] > 5:
                del self.pheromone_grid[position]
                # print(f"pheromone at {position} decayed after 5 seconds")

    def respawn_resources(self):
        current_time = time.time()
        if current_time - self.respawn_timer >= 1:  # respawn every [1,2,3,4,5,6,7,8,.....] seconds
            for _ in range(self.respawn_count):
                self.add_resource()
            self.respawn_timer = current_time  # reset the timer after all resources are added
            # print(f"resources respawned. Total resources: {len(self.resources)}")
