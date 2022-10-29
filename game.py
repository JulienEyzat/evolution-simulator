import random
import matplotlib.pyplot as plt
import tqdm

import environment
import animal

class Game:
    def __init__(self):
        self.max_x = 10
        self.max_y = 10
        self.nb_animals = 1
        self.environment = environment.Environment(self.max_x, self.max_y)
        self.animals = [ animal.Animal(random.randint(0, self.max_x), random.randint(0, self.max_y)) for i in range(self.nb_animals) ]

    def play_tour(self):
        dead_animal_indexes = []
        for index, current_animal in enumerate(self.animals):
            current_animal.generate_random_movement(self.max_x, self.max_y)
            if self.environment.can_eat_grass(current_animal.x, current_animal.y):
                self.environment.eat_grass(current_animal.x, current_animal.y)
            else:
                current_animal.loss_health()
            if current_animal.health <= 0:
                dead_animal_indexes.append(index)
            current_animal.regenerate_health()
        self.environment.grass_regeneration()

        for dead_animal_index in dead_animal_indexes:
            self.animals.pop()
            self.nb_animals-=1

    def plot_game(self):
        plt.cla()
        animals_x = [ current_animal.x for current_animal in self.animals ]
        animals_y = [ current_animal.y for current_animal in self.animals ]
        plt.scatter(x=animals_x, y=animals_y, color="w")
        plt.imshow(self.environment.grass)
        plt.pause(0.0001)
        plt.draw()

    def run(self):
        for i in tqdm.tqdm(range(1000)):
            self.play_tour()
            self.plot_game()

if __name__ == "__main__":
    game = Game()
    game.run()