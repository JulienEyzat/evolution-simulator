import numpy as np
import collections
import random

import animal

class Environment():
    def __init__(self):
        self.x_size = 30
        self.y_size = 30
        self.regenerated_grass_quantity = 0.003
        self.nb_animals = 30

        self.mutation_factor = 0.8
        self.similarity_factor = 0.1

        self.grass = np.ones((self.x_size, self.y_size))
        self.animals = [ self.generate_animal() for i in range(self.nb_animals) ]

    def update_environment(self):
        # Animals move in the environment
        self.animal_movement()
        # Animals reproduce
        self.animal_reproduction()
        # Animals eat grass if it can
        self.animal_eating_grass()
        # Animals fight
        self.animal_fights()
        # Loss health
        self.animal_hunger()
        # Natural regeneration
        self.animal_regeneration()
        # Grass regenerates in the environnement
        self.environment_grass_regeneration()
        # Animals die
        self.animal_die()

    def animal_movement(self):
        for index, current_animal in enumerate(self.animals):
            current_animal.generate_random_movement(self.x_size, self.y_size)
    
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

    def animal_reproduction(self):
        # Get list of animals to reproduce
        duplicated_animals = self.get_dict_animals_on_same_position()
        # Reproduce animals
        for (x, y), to_reproduce_animals in duplicated_animals.items():
            if self.are_animals_similar(to_reproduce_animals) and to_reproduce_animals[0].satiation == 1 and to_reproduce_animals[1].satiation == 1:
                self.animals.append(self.generate_animal(to_reproduce_animals))
                self.nb_animals += 1

    def animal_eating_grass(self):
        for index, current_animal in enumerate(self.animals):
            if current_animal.carnivorism < 0.5 and self.grass[current_animal.y, current_animal.x] >= current_animal.eaten_grass_quantity:
                self.grass[current_animal.y, current_animal.x] -= current_animal.eaten_grass_quantity
                current_animal.gain_satiation()
            else:
                current_animal.loss_satiation()

    def animal_fights(self):
        # Get list of animals to fight
        duplicated_animals = self.get_dict_animals_on_same_position()
        # Fight
        for (x, y), to_fight_animals in duplicated_animals.items():
            if to_fight_animals[0].carnivorism > to_fight_animals[1].carnivorism and to_fight_animals[0].carnivorism > 0.5:
                to_fight_animals[1].health = 0
                to_fight_animals[0].gain_satiation()
            elif to_fight_animals[1].carnivorism > to_fight_animals[0].carnivorism and to_fight_animals[1].carnivorism > 0.5:
                to_fight_animals[0].health = 0
                to_fight_animals[1].gain_satiation()
                
    def animal_hunger(self):
        for index, current_animal in enumerate(self.animals):
            if current_animal.satiation == 0:
                current_animal.loss_health()

    def animal_regeneration(self):
        for index, current_animal in enumerate(self.animals):
            if current_animal.satiation != 0:
                current_animal.gain_health()

    def environment_grass_regeneration(self):
        self.grass += self.regenerated_grass_quantity
        self.grass = np.where(self.grass <= 1, self.grass, 1)

    def animal_die(self):
        dead_animal_indexes = []
        for index, current_animal in enumerate(self.animals):
            if current_animal.health <= 0:
                dead_animal_indexes.append(index)
        for dead_animal_index in sorted(dead_animal_indexes, reverse=True):
            del self.animals[dead_animal_index]
            self.nb_animals-=1