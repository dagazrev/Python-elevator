import pygame
import os
from time import sleep

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# class that creates the screen and call the draw method
# of all the elements
class Window:
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 800
    FPS = 30

    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Font initialization
        font = pygame.font.SysFont('Arial', 40)

        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # clock
        self.fpsClock = pygame.time.Clock()

        self.objects = [[0] for _ in range(11)]

        self.running = True

    def add_object(self, object, layer=0):
        if layer >= 10:
            layer = 10
        if layer < 0:
            layer = 0
        if self.objects[layer] == 0:
            self.objects[layer] = [object]
        else:
            self.objects[layer].append(object)

    def draw(self):
        while self.running:
            # for loop through the event queue
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == KEYDOWN:
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == K_ESCAPE:
                        self.running = False
                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == QUIT:
                    self.running = False

            self.screen.fill((255,255,255))

            # drawing all layers
            for layer in self.objects:
                for object in layer:
                    # if layer is not empty
                    if object != 0:
                        #drawing object
                        object.draw()

            # Update the display
            # pygame.display.flip()   
            pygame.display.update()   
        
            self.fpsClock.tick(self.FPS)







