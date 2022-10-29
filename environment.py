import numpy as np
import collections
import random

import animal

class Environment():
    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.grass = np.ones((x_size, y_size))
        self.eaten_grass_quantity = 0.2
        self.regenerated_grass_quantity = 0.1
        self.nb_animals = 5
        self.animals = [ self.generate_animal() for i in range(self.nb_animals) ]

        self.mutation_factor = 0.1

    def update_environment(self):
        dead_animal_indexes = []
        # Animals move in the environment
        for index, current_animal in enumerate(self.animals):
            current_animal.generate_random_movement(self.x_size, self.y_size)
        # Animals reproduce
        self.reproduce_animals()
        # Animals eat grass if it can, or loss health else
        for index, current_animal in enumerate(self.animals):
            if self.can_eat_grass(current_animal.x, current_animal.y):
                self.eat_grass(current_animal.x, current_animal.y)
            else:
                current_animal.loss_health()
        # Animals die
        for index, current_animal in enumerate(self.animals):
            if current_animal.health <= 0:
                dead_animal_indexes.append(index)
        # Animals regenerate
        for index, current_animal in enumerate(self.animals):
            current_animal.regenerate_health()
        # Grass regenerates in the environnement
        self.grass_regeneration()

        for dead_animal_index in dead_animal_indexes:
            self.animals.pop()
            self.nb_animals-=1
    
    def generate_animal(self, parents=None):
        if parents:
            x = parents[0].x
            y = parents[0].y
            hunger_health_loss = np.mean([parents[0].hunger_health_loss, parents[1].hunger_health_loss]) + random.uniform(-self.mutation_factor, self.mutation_factor)
        else:
            x = random.randint(0, self.x_size)
            y = random.randint(0, self.y_size)
            hunger_health_loss = 0.1
        return animal.Animal(x, y, hunger_health_loss=hunger_health_loss)

    def get_dict_animals_on_same_position(self):
        animals_positions = [ (current_animal.x, current_animal.y) for current_animal in self.animals ]
        cnt = collections.Counter(animals_positions)
        positions_with_multiple_animals = [ key for key in cnt.keys() if cnt[key] > 1 ]
        duplicated_animals = collections.defaultdict(list)
        for i, v in enumerate(animals_positions):
            if v in positions_with_multiple_animals:
                duplicated_animals[v].append(self.animals[i])
        return duplicated_animals

    def reproduce_animals(self):
        # Get list of animals to reproduce
        duplicated_animals = self.get_dict_animals_on_same_position()
        # Reproduce animals
        for (x, y), to_reproduce_animals in duplicated_animals.items():
            self.animals.append(self.generate_animal(to_reproduce_animals))

    def can_eat_grass(self, x, y):
        if self.grass[y, x] >= self.eaten_grass_quantity:
            return True
        else:
            return False
    
    def eat_grass(self, x, y):
        self.grass[y, x] -= self.eaten_grass_quantity

    def grass_regeneration(self):
        self.grass += self.regenerated_grass_quantity
        self.grass = np.where(self.grass <= 1, self.grass, 1)
