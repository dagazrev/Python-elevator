import pygame 
import os
import random
from people_group import PeopleGroup

class Elevator:
    TIME_MOVING = 1
    TIME_OPEN = 1

    MAX_CHARGE = 1600
    MAX_FLOOR = 7

    IMG_EMPTY = "IMG_EMPTY"
    IMG_FULL = "IMG_FULL"

    STATE_MOVING = "MOVING"
    STATE_OPEN = "OPEN"
    STATE_CLOSE = "CLOSE"

    def __init__(self, window, floors, current_floor=0):
        self.window = window

        # floor
        self.current_floor = current_floor
        # self.next_floor = 2
        self.moving = 0
        self.floors = floors
        self.requested_floor = 0

        # state
        self.current_state = self.STATE_CLOSE
        self.open_counter = 0
        self.unit_open = self.TIME_OPEN / self.window.FPS

        # image
        self.current_img = self.IMG_EMPTY
        self.img_elevator = {}

        # people
        self.queue = []
        self.people = PeopleGroup()
        self.entered_people = 0
        self.exit_people = 0

        # position
        self.floor_distace = 94
        self.pos_y = 22 + self.floor_distace*self.current_floor
        self.pos_x = 300
        self.unit_moving = self.TIME_MOVING / self.window.FPS

        self.init_img_elevator()

    # control stuff
    def external_request(self, floor_number):
        print("Elevator: floor called %d " % floor_number)
        self.queue.append(floor_number)

    def internal_request(self, floor_number):
        print("Elevator: internal call %d " % floor_number)
        self.queue.append(floor_number)

    def change_state(self, state):
        print("Elevator: Stated changed: %s ---> %s"%(self.current_state, state))
        self.current_state = state
        if state == self.STATE_OPEN:
            self.open_counter = self.TIME_OPEN


        if self.current_floor == self.requested_floor:
            self.moving = 0

    def serve(self):
        if self.moving ==0 and len(self.queue)>0:
            self.requested_floor = self.queue.pop(0)
            print("Elevator: (1) call receaved from floor : %d" % self.requested_floor)
            if self.requested_floor == self.current_floor:
                print("Elevator: (1.1) called from the same floor, opening the door")
                self.open_door()
            else:
                self.moving = self.direction(self.requested_floor)
                self.change_state(self.STATE_MOVING)

        elif self.moving != 0:
            # elevator on a floor
            if  round(float(self.current_floor),4).is_integer():
                print("Elevator: (2) arrived to floor : ", int(round(self.current_floor,2)))
                self.current_floor = int(round(self.current_floor,2))
                if self.current_floor == self.requested_floor or self.current_floor in self.queue:
                    self.open_door()
                    if not self.is_full():
                        return 

            if self.moving > 0:
                if self.current_floor >= self.MAX_FLOOR:
                    self.moving = 0; 
                else:
                    self.current_floor = self.current_floor + self.unit_moving
            elif self.moving < 0:
                if self.current_floor <= 0:
                    self.moving = 0
                else:
                    self.current_floor = self.current_floor - self.unit_moving

    def direction(self, requested_floor):
        res = self.current_floor - requested_floor
        if res < 0:
            return 1
        else :
            return -1

    def is_full(self):
        return len(self.people) == 8 or (self.people.get_weight()+10 >= self.MAX_CHARGE)

    def open_door(self):
        self.change_state(self.STATE_OPEN)

        print("Elevator: (3) opening the door on floor %d" % self.current_floor)
        # removing people going out people going out
        people_going_out = self.people.get_exit_floor(self.current_floor)
        self.people.remove_sub_group(people_going_out)
        self.exit_people = self.exit_people + people_going_out.get_nb()
        self.queue = list(filter((self.current_floor).__ne__, self.queue))

        print("Elevator: (4) Nb people went out %d " % people_going_out.get_nb())

        # oppening the door in the floor and letting the people to go out
        # also obtaining the people that is entering
        if not self.is_full():
            new_people = self.floors[self.current_floor].open_door(people_going_out)
            
            # self.people.join(new_people)
            # self.entered_people = self.entered_people + new_people.get_nb()
            # print("Elevator: (5) Nb people entered %d " % new_people.get_nb())
            # print("Elevator: (6) Total people %d, current floor: %d \n\n" % (self.people.get_nb(), self.current_floor))

            # internal command
            nb_people_entered = 0
            for p in new_people:
                # if p.exit_floor != self.current_floor:
                if not self.is_full():
                    self.people.add_person(p)
                    nb_people_entered = nb_people_entered + 1
                    self.internal_request(p.exit_floor)
                else:
                    self.floors[self.current_floor].over_weight(new_people.get_last(nb_people_entered))
                    break
            self.entered_people = self.entered_people + nb_people_entered
            print("Elevator: (5) Nb people entered %d " % nb_people_entered)
            print("Elevator: (6) Total people %d, current floor: %d \n\n" % (self.people.get_nb(), self.current_floor))
            
            # the elevator should be called again for the people that could enter
            for p in new_people.get_last(nb_people_entered):
                self.external_request(p.enter_floor)

        else:
            print("Elevator: (5) canno take more people")


    # drawing stuff
    def init_img_elevator(self):
        # empty elevator
        img_empty = pygame.image.load(os.path.join('src','img', 'elevator_empty.png'))
        img_empty = pygame.transform.smoothscale(img_empty,(55, 95))
        # full elevator
        img_full = pygame.image.load(os.path.join('src','img', 'elevator_full.png'))
        img_full = pygame.transform.smoothscale(img_full,(55, 95))

        self.img_elevator = {self.IMG_EMPTY : img_empty,
                            self.IMG_FULL: img_full}

    def draw(self):
        if self.current_state == self.STATE_OPEN:
            self.open_counter = self.open_counter - self.unit_open
            if self.open_counter <= 0:
                if self.moving == 0:
                    self.change_state(self.STATE_CLOSE)
                else:
                    self.change_state(self.STATE_MOVING)
        else:
            self.serve()

        self.pos_y = 22 + self.floor_distace*self.current_floor
        if(len(self.people) > 0):
            self.window.screen.blit(self.img_elevator[self.IMG_FULL], (self.pos_x, self.pos_y))
        else:
            self.window.screen.blit(self.img_elevator[self.IMG_EMPTY], (self.pos_x, self.pos_y))
        
