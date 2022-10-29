import numpy as np
import collections
import random

import animal

class Environment():
    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.grass = np.ones((x_size, y_size))
        self.regenerated_grass_quantity = 0.3
        self.nb_animals = 10
        self.animals = [ self.generate_animal() for i in range(self.nb_animals) ]

        self.mutation_factor = 0.5
        self.similarity_factor = 0.1

    def update_environment(self):
        # Animals move in the environment
        for index, current_animal in enumerate(self.animals):
            current_animal.generate_random_movement(self.x_size, self.y_size)
        # Animals reproduce
        self.reproduce_animals()
        # Animals eat grass if it can, or loss health else
        for index, current_animal in enumerate(self.animals):
            if current_animal.carnivorism < 0.5:
                if self.can_eat_grass(current_animal):
                    self.eat_grass(current_animal)
                    current_animal.regenerate_health()
                else:
                    current_animal.loss_health()
        # Animals fight
        self.fight_animals()
        # Animals die
        dead_animal_indexes = []
        for index, current_animal in enumerate(self.animals):
            if current_animal.health <= 0:
                dead_animal_indexes.append(index)
        # Grass regenerates in the environnement
        self.grass_regeneration()

        for dead_animal_index in dead_animal_indexes:
            self.animals.pop()
            self.nb_animals-=1
    
    def generate_animal(self, parents=None):
        if parents:
            x = parents[0].x
            y = parents[0].y
            carnivorism = np.mean([parents[0].carnivorism, parents[1].carnivorism]) + random.uniform(-self.mutation_factor, self.mutation_factor)
            if carnivorism < 0:
                carnivorism = 0
            elif carnivorism > 1:
                carnivorism = 1
        else:
            x = random.randint(0, self.x_size)
            y = random.randint(0, self.y_size)
            carnivorism = 0
        return animal.Animal(x, y, carnivorism=carnivorism)

    def get_dict_animals_on_same_position(self):
        animals_positions = [ (current_animal.x, current_animal.y) for current_animal in self.animals ]
        cnt = collections.Counter(animals_positions)
        positions_with_multiple_animals = [ key for key in cnt.keys() if cnt[key] > 1 ]
        duplicated_animals = collections.defaultdict(list)
        for i, v in enumerate(animals_positions):
            if v in positions_with_multiple_animals:
                duplicated_animals[v].append(self.animals[i])
        return duplicated_animals

    def are_animals_similar(self, animals):
        return animals[1].carnivorism - self.similarity_factor <= animals[0].carnivorism <= animals[1].carnivorism + self.similarity_factor

    def reproduce_animals(self):
        # Get list of animals to reproduce
        duplicated_animals = self.get_dict_animals_on_same_position()
        # Reproduce animals
        for (x, y), to_reproduce_animals in duplicated_animals.items():
            if self.are_animals_similar(to_reproduce_animals):
                self.animals.append(self.generate_animal(to_reproduce_animals))

    def fight_animals(self):
        # Get list of animals to fight
        duplicated_animals = self.get_dict_animals_on_same_position()
        # Fight
        for (x, y), to_fight_animals in duplicated_animals.items():
            if to_fight_animals[0].carnivorism > to_fight_animals[1].carnivorism and to_fight_animals[0].carnivorism > 0.5:
                to_fight_animals[1].health = 0
                to_fight_animals[0].regenerate_health()
                # print("death by fight")
            elif to_fight_animals[1].carnivorism > to_fight_animals[0].carnivorism and to_fight_animals[1].carnivorism > 0.5:
                to_fight_animals[0].health = 0
                to_fight_animals[1].regenerate_health()
                # print("death by fight")
                
    def can_eat_grass(self, current_animal):
        return self.grass[current_animal.y, current_animal.x] >= current_animal.eaten_grass_quantity
    
    def eat_grass(self, current_animal):
        self.grass[current_animal.y, current_animal.x] -= current_animal.eaten_grass_quantity

    def grass_regeneration(self):
        self.grass += self.regenerated_grass_quantity
        self.grass = np.where(self.grass <= 1, self.grass, 1)
