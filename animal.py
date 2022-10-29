import random

class Animal():
    def __init__(self, x, y, hunger_health_loss=0.1):
        self.x = x
        self.y = y
        self.max_movement = 2
        self.health = 1
        self.hunger_health_loss = hunger_health_loss
        self.regenerated_health = 0.01
    
    def move(self, x, y):
        self.x = x
        self.y = y

    def loss_health(self):
        self.health -= self.hunger_health_loss

    def generate_random_movement(self, max_x, max_y):
        new_x = self.x + random.randint(-self.max_movement, self.max_movement)
        if new_x >= max_x:
            new_x = max_x - 1
        elif new_x < 0:
            new_x = 0
        new_y = self.y + random.randint(-self.max_movement, self.max_movement)
        if new_y >= max_y:
            new_y = max_y - 1
        elif new_y < 0:
            new_y = 0

        self.move(new_x, new_y)

    def regenerate_health(self):
        self.health += self.regenerated_health
        if self.health > 1:
            self.health = 1