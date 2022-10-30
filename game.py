import matplotlib.pyplot as plt
import tqdm

import numpy as np

import environment

class Game:
    def __init__(self):
        self.environment = environment.Environment()
        self.i = 0

    def plot_game(self):
        plt.cla()
        animals_x = [ current_animal.x for current_animal in self.environment.animals ]
        animals_y = [ current_animal.y for current_animal in self.environment.animals ]
        animals_color = [ current_animal.carnivorism for current_animal in self.environment.animals ]
        plt.scatter(x=animals_x, y=animals_y, c=animals_color)
        plt.imshow(self.environment.grass)
        texts = {
            "Nb tours": self.i,
            "Nb carnivors": len([ carnivorism for carnivorism in animals_color if carnivorism > 0.5 ]),
            "Nb herbivors": len([ carnivorism for carnivorism in animals_color if carnivorism <= 0.5 ]),
            "Mean carnivorism": np.mean(animals_color),
            "Std carnivorism": np.std(animals_color)
        }
        i = 0
        for key, value in texts.items():
            plt.text(0.1, 0.75-i*0.02, "%s : %s" %(key, value), fontsize=14, transform=plt.gcf().transFigure)
            i+=1
        plt.pause(0.1)
        plt.draw()

    def run(self):
        for i in range(1000):
            self.i = i
            self.environment.update_environment()
            self.plot_game()
            # print(self.environment.animals)
            # hunger_health_loss_mean = np.mean([ animal.hunger_health_loss for animal in self.environment.animals ])
            # print(hunger_health_loss_mean)

if __name__ == "__main__":
    game = Game()
    game.run()