import random

class Animal():
    def __init__(self, x, y, carnivorism=0):
        self.x = x
        self.y = y
        self.max_movement = 2

        self.carnivorism = carnivorism
        self.eaten_grass_quantity = 0.6 - self.carnivorism
        if self.eaten_grass_quantity < 0:
            self.eaten_grass_quantity = 0

        self.satiation = 1
        self.satiation_loss = 0.75 - self.carnivorism*0.5
        self.satiation_grass_gain = 1 - self.carnivorism
        self.satiation_animal_gain = self.carnivorism

        self.health = 1
        self.health_loss = 0.2
        self.health_gain = 0.05

    def loss_satiation(self):
        self.satiation -= self.satiation_loss
        if self.satiation < 0:
            self.satiation = 0

    def gain_satiation(self, food_type):
        if food_type == "grass":
            self.satiation += self.satiation_grass_gain
        elif food_type == "animal":
            self.satiation += self.satiation_animal_gain
        if self.satiation > 1:
            self.satiation = 1

    def loss_health(self):
        self.health -= self.health_loss
        if self.health < 0:
            self.health = 0

    def gain_health(self):
        self.health += self.health_gain
        if self.health > 1:
            self.health = 1

    def move(self, x, y):
        self.x = x
        self.y = y

    def generate_random_movement(self):
        new_x = self.x + random.randint(-self.max_movement, self.max_movement)
        new_y = self.y + random.randint(-self.max_movement, self.max_movement)
        return new_x, new_y