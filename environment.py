import numpy as np
import collections
import random

import animal

class Environment():
    def __init__(self):
        self.x_size = 15
        self.y_size = 15
        self.regenerated_grass_quantity = 0.1
        self.nb_animals = 30

        self.mutation_factor = 0.2
        self.similarity_factor = 0.1
        self.reproduction_factor = 0.2

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

    def can_move(self, new_x, new_y):
        if new_x >= self.x_size or new_x < 0:
            return False
        if new_y >= self.y_size or new_y < 0:
            return False
        number_of_animals_on_expected_pos = len([ 1 for current_animal in self.animals if current_animal.x == new_x and current_animal.y == new_y ])
        if number_of_animals_on_expected_pos > 2:
            return False
        return True

    def animal_movement(self):
        for index, current_animal in enumerate(self.animals):
            new_x, new_y = current_animal.generate_random_movement()
            if self.can_move(new_x, new_y):
                current_animal.move(new_x, new_y)

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
            x = random.randint(0, self.x_size-1)
            y = random.randint(0, self.y_size-1)
            carnivorism = 0.1
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
            satiation_cond = to_reproduce_animals[0].satiation == 1 and to_reproduce_animals[1].satiation == 1
            reproduction_cond = random.random() >= self.reproduction_factor
            similarity_cond = self.are_animals_similar(to_reproduce_animals)
            number_cond = len(to_reproduce_animals) == 2
            if similarity_cond and satiation_cond and number_cond and reproduction_cond:
                self.animals.append(self.generate_animal(to_reproduce_animals))
                self.nb_animals += 1

    def animal_eating_grass(self):
        for index, current_animal in enumerate(self.animals):
            if current_animal.eaten_grass_quantity > 0 and self.grass[current_animal.y, current_animal.x] >= current_animal.eaten_grass_quantity:
                self.grass[current_animal.y, current_animal.x] -= current_animal.eaten_grass_quantity
                current_animal.gain_satiation("grass")
            else:
                current_animal.loss_satiation()

    def animal_fights(self):
        # Get list of animals to fight
        duplicated_animals = self.get_dict_animals_on_same_position()
        # Fight
        for _, to_fight_animals in duplicated_animals.items():
            animal0_win_cond = to_fight_animals[0].carnivorism - 2*0.2 < to_fight_animals[1].carnivorism < to_fight_animals[0].carnivorism - 0.2
            animal1_win_cond = to_fight_animals[1].carnivorism - 2*0.2 < to_fight_animals[0].carnivorism < to_fight_animals[1].carnivorism - 0.2
            if animal0_win_cond:
                to_fight_animals[1].health = 0
                to_fight_animals[0].gain_satiation("animal")
            elif animal1_win_cond:
                to_fight_animals[0].health = 0
                to_fight_animals[1].gain_satiation("animal")
                
    def animal_hunger(self):
        for index, current_animal in enumerate(self.animals):
            if current_animal.satiation < 0.5:
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