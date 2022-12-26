# Import the pygame module
import pygame
import os
from time import sleep
from people_group import PeopleGroup
from person import Person
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

class Building:
    def __init__(self, screen):
        self.screen = screen
        # designing building
        self.img_building = pygame.image.load(os.path.join('src','img', 'building.png'))
        self.img_building = pygame.transform.smoothscale(self.img_building,(300, SCREEN_HEIGHT))

    def draw(self):
        screen.blit(self.img_building, (0,0))


class Elevator:
    def __init__(self, screen, fps=25):
        self.screen = screen
        self.fps = fps

        self.current_state = "eb"
        self.img_elevator = {}
        self.max_floor = 7

        self.current_floor = 0
        self.next_floor = 2
        self.moving = 1
        

        self.floor_distace = 94
        self.time_floor_to_floor = 1
        self.unit_increase = self.time_floor_to_floor / self.fps

        self.pos_y = 22 + self.floor_distace*self.current_floor
        self.pos_x = 300

        self.init_img_elevator()

    def init_img_elevator(self):
        # empty open elevator
        eo = pygame.image.load(os.path.join('src','img', 'elevator_empty_open.png'))
        eo = pygame.transform.smoothscale(eo,(55, 95))
        # empty busy elevator
        eb = pygame.image.load(os.path.join('src','img', 'elevator_empty_busy.png'))
        eb = pygame.transform.smoothscale(eb,(55, 95))
        # full open elevator
        fo = pygame.image.load(os.path.join('src','img', 'elevator_full_open.png'))
        fo = pygame.transform.smoothscale(fo,(55, 95))
        # full busy elevator
        fb = pygame.image.load(os.path.join('src','img', 'elevator_full_busy.png'))
        fb = pygame.transform.smoothscale(fb,(55, 95))

        self.img_elevator = {"eo":eo, "eb":eb, "fo":fo, "fb":fb}

    def cal_elevator_floor(self):
        if self.moving != 0:
            # elevator arrived
            if round(self.current_floor,2) == self.next_floor:
                self.moving = 0
                self.current_state = "eo"

            # elevator on a floor
            if  isinstance(self.current_floor, int) or round(self.current_floor,2).is_integer():
                print("arrived: ", int(round(self.current_floor,2)))

            if self.moving > 0:
                if self.current_floor >= self.max_floor:
                    self.moving = 0; 
                else:
                    self.current_floor = self.current_floor + self.unit_increase
            elif self.moving < 0:
                if self.current_floor <= 0:
                    self.moving = 0
                else:
                    self.current_floor = self.current_floor - self.unit_increase


    def change_state(self, state):
        self.current_state = state

    def draw(self):
        # self.pos_y = self.pos_y + self.cal_elevator_pos()
        self.cal_elevator_floor()
        self.pos_y = 22 + self.floor_distace*self.current_floor
        screen.blit(self.img_elevator[self.current_state], (self.pos_x, self.pos_y))

class Floor:
    def __init__(self, nb, screen, fps=25):
        self.nb = nb
        self.x = 275
        self.y = 50 + self.nb*94
        self.people_group = PeopleGroup([])
        self.create_people()

    def create_people(self):
        nb_people = random.randint(0,3)
        for i in range(nb_people):
            person = Person(self.nb, ((self.nb + 1) % 8),  weight=random.randint(45,90), gender=bool(random.getrandbits(1)) )
            self.people_group.add_person(person)


    def draw(self):
        p_i = 0
        p_space = 25
        for p in self.people_group:
            screen.blit(p.img, (self.x-p_i*p_space, self.y))
            p_i = p_i + 1



if __name__ == '__main__':

    # Initialize pygame
    pygame.init()

    # Font initialization
    font = pygame.font.SysFont('Arial', 40)

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # frames of the game
    fps = 25
    fpsClock = pygame.time.Clock()


    building = Building(screen)
    elevator = Elevator(screen, fps)

    floors = []
    for i in range(8):
        floors.append(Floor(i, screen, fps))

    # Variable to keep the main loop running
    running = True
    while running:
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False

        screen.fill((255,255,255))
        building.draw()
        elevator.draw()
        for f in floors:
            f.draw()
        # Update the display
        # pygame.display.flip()   
        pygame.display.update()   
        

        fpsClock.tick(fps)























# # Import the pygame module
# import pygame
# import os
# from time import sleep

# # Import pygame.locals for easier access to key coordinates
# # Updated to conform to flake8 and black standards
# from pygame.locals import (
#     K_ESCAPE,
#     KEYDOWN,
#     QUIT,
# )

# # Define constants for the screen width and height
# SCREEN_WIDTH = 600
# SCREEN_HEIGHT = 800

# class Building:
#     def __init__(self, screen):
#         self.screen = screen
#         # designing building
#         self.img_building = pygame.image.load(os.path.join('src','img', 'building.png'))
#         self.img_building = pygame.transform.scale(self.img_building,(300, SCREEN_HEIGHT))

#     def draw(self):
#         screen.blit(self.img_building, (0,0))


# class Elevator:
#     def __init__(self, screen, fps=25):
#         self.screen = screen
#         self.fps = fps

#         self.img_elevator = pygame.image.load(os.path.join('src','img', 'elevator_empty_open.png'))
#         self.img_elevator = pygame.transform.scale(self.img_elevator,(55, 95))

#         self.current_floor = 0
#         self.next_floor = 1
#         self.moving = 1

#         self.floor_distace = 94
#         self.time_floor_to_floor = 1
#         self.unit_increase = self.floor_distace / (self.fps*self.time_floor_to_floor)

#         self.pos_y = 22 + self.floor_distace*self.current_floor
#         self.pos_x = 300


#     def cal_elevator_pos(self):
#         print((self.pos_y - 22)/self.floor_distace)
#         if ((self.pos_y - 22)/self.floor_distace) >= self.next_floor:
#             self.moving = 0
#             return 0

#         if self.moving > 0:
#             return self.unit_increase
#         elif self.moving < 0:
#             return -self.unit_increase
#         return 0

#     def draw(self):
#         self.pos_y = self.pos_y + self.cal_elevator_pos()
#         screen.blit(self.img_elevator, (self.pos_x, self.pos_y))

        

# if __name__ == '__main__':

#     # Initialize pygame
#     pygame.init()

#     # Font initialization
#     font = pygame.font.SysFont('Arial', 40)

#     # Create the screen object
#     # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#     # frames of the game
#     fps = 25
#     fpsClock = pygame.time.Clock()


#     building = Building(screen)
#     elevator = Elevator(screen, fps)

#     # Variable to keep the main loop running
#     running = True
#     while running:
#         # for loop through the event queue
#         for event in pygame.event.get():
#             # Check for KEYDOWN event
#             if event.type == KEYDOWN:
#                 # If the Esc key is pressed, then exit the main loop
#                 if event.key == K_ESCAPE:
#                     running = False
#             # Check for QUIT event. If QUIT, then set running to false.
#             elif event.type == QUIT:
#                 running = False

#         screen.fill((255,255,255))
#         building.draw()
#         elevator.draw()
#         # Update the display
#         # pygame.display.flip()   
#         pygame.display.update()   
        

#         fpsClock.tick(fps)

