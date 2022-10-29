import matplotlib.pyplot as plt
import tqdm

import numpy as np

import environment

class Game:
    def __init__(self):
        self.max_x = 10
        self.max_y = 10
        self.environment = environment.Environment(self.max_x, self.max_y)

    def plot_game(self):
        plt.cla()
        animals_x = [ current_animal.x for current_animal in self.environment.animals ]
        animals_y = [ current_animal.y for current_animal in self.environment.animals ]
        plt.scatter(x=animals_x, y=animals_y, color="w")
        plt.imshow(self.environment.grass)
        plt.pause(0.0001)
        plt.draw()

    def run(self):
        for i in tqdm.tqdm(range(1000)):
            self.environment.update_environment()
            self.plot_game()
            # hunger_health_loss_mean = np.mean([ animal.hunger_health_loss for animal in self.environment.animals ])
            # print(hunger_health_loss_mean)

if __name__ == "__main__":
    game = Game()
    game.run()