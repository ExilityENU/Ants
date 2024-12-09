import networkx as nx
import random
import time

class Environment:
    """Graph-based environment with terrain and timed resource respawn."""
    def __init__(self, grid_size, num_resources, respawn_count=5):
        self.graph = nx.Graph()
        self.grid_size = grid_size
        self.nest = (grid_size // 2, grid_size // 2)
        self.resources = []
        self.respawn_timer = time.time()  # Track time for resource respawn
        self.respawn_count = respawn_count  # Number of resources to respawn at a time
        self.terrain = {}  # Store terrain types
        self._initialize_graph()
        self._generate_terrain()
        self._place_resources(num_resources)

    def _initialize_graph(self):
        # Add nodes for each grid cell
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                self.graph.add_node((x, y))
        # Add edges between adjacent nodes (4-connectivity)
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                        self.graph.add_edge((x, y), (nx, ny), weight=1.0)

    def _generate_terrain(self):
        # Terrain types: Grass (1.0), Water (impassable), Rocks (2.0)
        terrain_types = ["grass", "water", "rock"]
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                terrain = random.choice(terrain_types)
                self.terrain[(x, y)] = terrain
                if terrain == "water":
                    # Remove impassable nodes from the graph
                    self.graph.remove_node((x, y))
                elif terrain == "rock":
                    # Increase traversal cost for rocky terrain
                    for neighbor in list(self.graph.neighbors((x, y))):
                        if self.graph.has_edge((x, y), neighbor):
                            self.graph[(x, y)][neighbor]["weight"] = 2.0

    def _place_resources(self, num_resources):
        for _ in range(num_resources):
            self.add_resource()

    def add_resource(self):
        while True:
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if (x, y) != self.nest and (x, y) in self.graph.nodes:
                resource_type = random.choice(["food", "water", "energy"])
                utility = {"food": 10, "water": 5, "energy": 3}[resource_type]
                self.resources.append({"pos": (x, y), "type": resource_type, "utility": utility})
                break

    def respawn_resources(self):
        # Check if 5 seconds have passed
        if time.time() - self.respawn_timer >= 5:
            for _ in range(self.respawn_count):
                self.add_resource()
            self.respawn_timer = time.time()

    def decay_pheromones(self):
        for u, v, data in self.graph.edges(data=True):
            data['weight'] = max(1.0, data['weight'] - 0.01)

    def add_pheromone(self, path):
        for i in range(len(path) - 1):
            self.graph[path[i]][path[i + 1]]['weight'] += 1.0
