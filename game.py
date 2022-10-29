import matplotlib.pyplot as plt
import tqdm

import numpy as np

import environment

class Game:
    def __init__(self):
        self.max_x = 30
        self.max_y = 30
        self.environment = environment.Environment(self.max_x, self.max_y)

    def plot_game(self):
        plt.cla()
        animals_x = [ current_animal.x for current_animal in self.environment.animals ]
        animals_y = [ current_animal.y for current_animal in self.environment.animals ]
        animals_color = [ current_animal.carnivorism for current_animal in self.environment.animals ]
        # print(animals_color)
        plt.scatter(x=animals_x, y=animals_y, c=animals_color)
        plt.imshow(self.environment.grass)
        plt.pause(0.1)
        plt.draw()

    def run(self):
        for i in tqdm.tqdm(range(1000)):
            self.environment.update_environment()
            self.plot_game()
            # print(self.environment.animals)
            # hunger_health_loss_mean = np.mean([ animal.hunger_health_loss for animal in self.environment.animals ])
            # print(hunger_health_loss_mean)

if __name__ == "__main__":
    game = Game()
    game.run()