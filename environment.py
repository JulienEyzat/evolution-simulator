import numpy as np

class Environment():
    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.grass = np.ones((x_size, y_size))
        self.eaten_grass_quantity = 0.5
        self.regenerated_grass_quantity = 0.1
    
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