import pygame 
import os
import random
class Person:
    def __init__(self, enter_floor, exit_floor, weight=60, gender=True, age=32):
        self.weight = weight
        self.gender = gender
        self.age = age
        self.enter_floor = enter_floor
        self.exit_floor = exit_floor

        style = str(random.randint(1,3))

        if gender:
            self.img = pygame.image.load(os.path.join('src','img', 'm'+style+'.png'))
        else:
            self.img = pygame.image.load(os.path.join('src','img', 'f'+style+'.png'))
        self.img = pygame.transform.smoothscale(self.img,(20, 60))

    def __str__(self):
        return "[Enter: %d, Exit: %d]"%(self.enter_floor, self.exit_floor)


