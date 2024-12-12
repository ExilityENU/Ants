import networkx as nx
import random
import time


class Environment:
    def __init__(self, grid_size, num_resources, respawn_count=3, num_colonies=2):
        self.graph = nx.Graph()
        self.grid_size = grid_size
        self.nests = []
        self.resources = []
        self.respawn_timer = time.time()
        self.respawn_count = respawn_count
        self.terrain = {}
        self.pheromone_grid = {}
        self.colony_food_count = {i: 0 for i in range(num_colonies)}  # Track food count for each colony
        self._initialize_graph()
        self._generate_terrain()
        self._place_nests(num_colonies)
        self._place_resources(num_resources)

    def _initialize_graph(self):
        directions = [
            (1, 0), (0, 1), (-1, 0), (0, -1),  # Cardinal directions
            (1, 1), (-1, -1), (1, -1), (-1, 1)  # Diagonal directions (if allowed)
        ]
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                self.graph.add_node((x, y))
                for dx, dy in directions:
                    next_x, next_y = x + dx, y + dy
                    if 0 <= next_x < self.grid_size and 0 <= next_y < self.grid_size:
                        self.graph.add_edge((x, y), (next_x, next_y), weight=1.0)

    def _generate_terrain(self):
        terrain_weights = {"grass": 0.45, "rock": 0.45, "water": 0.10}  # 35% both grass and rocks 30% water
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

    def _place_nests(self, num_colonies):
        for _ in range(num_colonies):
            while True:
                x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
                if self.terrain.get((x, y)) == "grass" and (x, y) not in self.nests:
                    self.nests.append((x, y))
                    break

    def _place_resources(self, num_resources):
        for _ in range(num_resources):
            self.add_resource()

    def add_resource(self):
        while True:
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if (x, y) not in self.nests and (x, y) in self.graph.nodes:
                resource_type = random.choice(["food", "water", "energy"])
                utility = {"food": 10, "water": 5, "energy": 3}[resource_type]
                self.resources.append({"pos": (x, y), "type": resource_type, "utility": utility})
                # print(f"Resource added: {resource_type} at ({x}, {y})")  # Debug log
                break

    def add_pheromone(self, path):
        current_time = time.time()
        for position in path:
            self.pheromone_grid[position] = current_time
            # print(f"Pheromone added at {position} at time {current_time}")

    def decay_pheromones(self):
        current_time = time.time()
        for position in list(self.pheromone_grid.keys()):
            if current_time - self.pheromone_grid[position] > 5:
                del self.pheromone_grid[position]
                # print(f"Pheromone at {position} decayed after 5 seconds")

    def respawn_resources(self):
        current_time = time.time()
        if current_time - self.respawn_timer >= 5:  # Respawn every 5 seconds
            for _ in range(self.respawn_count):  # Add `respawn_count` resources
                self.add_resource()
            self.respawn_timer = current_time  # Reset the timer after all resources are added
            # print(f"Resources respawned. Total resources: {len(self.resources)}")
