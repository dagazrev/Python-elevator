import pygame 
import os
from people_group import PeopleGroup
import threading
 
# this class model the elevator
# contains the neccesary functions to desing and control the the elevator
class Elevator:
    lock = threading.Lock()

    # time (in seconds) to travel from a floor to another 
    TIME_MOVING = 1
    # time (in seconds) to stay on a floor with the door opened 
    TIME_OPEN = 1

    # max supported change of the elevator
    MAX_CHARGE = 1600
    # max number of people supported inside the elevator
    MAX_PEOPLE = 8

    # images of the elevator
    IMG_EMPTY = "IMG_EMPTY"
    IMG_FULL = "IMG_FULL"

    # states of the elevator
    # STATE_OPEN: elevator is open on a floor
    # STATE_MOVING : elevator is moving
    # STATE_WATING: elevator is waiting for a call
    STATE_MOVING = "MOVING"
    STATE_OPEN = "OPEN"
    STATE_WATING = "CLOSE"

    DISTANCE_FLOOR = 94.0

    def __init__(self, window, floors, screen_info, current_floor=0):
        self.window = window

        # floor
        self.current_floor = current_floor
        self.direction = 0
        self.floors = floors
        self.requested_floor = 0

        # state
        self.current_state = self.STATE_WATING
        self.open_counter = 0
        # image
        self.current_img = self.IMG_EMPTY
        self.img_elevator = {}

        # people
        self.queue = []
        self.people = PeopleGroup()
        self.entered_people = 0
        self.exit_people = 0

        # position
        self.pos_y = 24 + self.DISTANCE_FLOOR*self.current_floor
        self.pos_x = 300
        self.moving_counter = 0

        # screen info
        self.screen_info = screen_info

        # used to stop the application
        self.is_working = True

        # if true, the elevator will print in the terminal all the steps 
        self.talkative = True

        # emergency
        self.emergency = False

        # charge elevator
        self.init_img_elevator()

    # Obtain external calls frm the floors
    def external_request(self, floor_number):
        self.talk("floor called %d " % floor_number)
        self.__request(floor_number)

    # Obtain internal calls from the inside of the elevator
    def internal_request(self, floor_number):
        if floor_number < 0:
            self.talk("EMERGENCI CALLED !!!!!!!!!!!", True)
            self.emergency = True
        self.talk("internal call %d " % floor_number)
        self.__request(floor_number)

    # Quque calls
    # two threads can access to this function (elevator_th (main thread) and floors_th)
    # to avoid concurrence, is accessible by only one thread at a time
    def __request(self, floor_number):
        self.lock.acquire()
        self.queue.append(floor_number)
        self.lock.release()

    # Change the state of the elevaotor
    def change_state(self, state):
        self.talk("Stated changed: %s ---> %s\n\n"%(self.current_state, state))
        if state == self.STATE_OPEN:
            self.open_counter = self.TIME_OPEN
        elif state == self.STATE_MOVING:
            self.moving_counter = self.TIME_MOVING

        if state != self.TIME_MOVING and self.current_floor == self.requested_floor:
            self.direction = 0

        self.current_state = state

    # Core of the elevator
    # control the states and respond to the calls
    def serve(self):
        # check if the elevator is open to decrease the opening time
        if self.current_state == self.STATE_OPEN:
            self.open_counter = self.open_counter - 1/self.window.FPS
            if self.open_counter <= 0:
                if self.direction == 0:
                    self.change_state(self.STATE_WATING)
                else:
                    self.change_state(self.STATE_MOVING)
                self.floors[self.current_floor].close_door()

        # check if the elevator is waiting and the queue is not empty to respond to the first call
        elif self.current_state == self.STATE_WATING and len(self.queue)>0:
            self.lock.acquire() #
            self.requested_floor = self.queue.pop(0)
            self.lock.release() #
            self.talk("(1) call receaved from floor : %d" % self.requested_floor)
            
            if self.requested_floor == self.current_floor:
                self.talk("(1.1) called from the same floor, opening the door")
                self.open_door()
            else:
                self.direction = self.get_direction(self.requested_floor)
                self.change_state(self.STATE_MOVING)

        # check if the elevator reach a requested  floor while is moving
        elif self.current_state == self.STATE_MOVING:
            # elevator on a floor
            if  self.moving_counter <= 0:
                self.moving_counter = 0
                self.current_floor = self.current_floor + self.direction
                self.talk("(2) arrived to floor : %d" % self.current_floor)                    
                if self.current_floor == self.requested_floor or self.current_floor in self.queue:
                    self.open_door()                        
                else:
                    self.change_state(self.STATE_MOVING)
            else:
                self.moving_counter = self.moving_counter - 1/self.window.FPS

    # return the direction of the elevator
    def get_direction(self, requested_floor):
        res = self.current_floor - requested_floor
        if res < 0:
            return 1
        else :
            return -1

    # return true if the elevator cannot take more people
    def is_full(self, p_weight=0):
        return ((len(self.people) == self.MAX_PEOPLE) or (self.people.get_weight()+p_weight >= self.MAX_CHARGE))

    # actions when the elevator reach a floor
    def open_door(self):
        self.change_state(self.STATE_OPEN)

        self.talk("(3) opening the door on floor %d" % self.current_floor)

        # removing people going out people going out
        people_going_out = self.people.get_exit_floor(self.current_floor)
        self.people.remove_sub_group(people_going_out)
        self.exit_people = self.exit_people + people_going_out.get_nb()
        self.lock.acquire()
        self.queue = list(filter((self.current_floor).__ne__, self.queue))
        self.lock.release()
        self.talk("(4) Nb people went out %d " % people_going_out.get_nb())

        # oppening the door in the floor and letting the people to go out
        # also obtaining the people that is entering
        if not self.is_full():
            new_people = self.floors[self.current_floor].open_door(people_going_out)

            # internal command
            nb_people_entered = 0
            for p in new_people:
                # if p.exit_floor != self.current_floor:
                if not self.is_full(p.weight):
                    self.people.add_person(p)
                    nb_people_entered = nb_people_entered + 1
                    self.internal_request(p.exit_floor)
                else:
                    self.floors[self.current_floor].over_weight(new_people.get_last(nb_people_entered))
                    break
            self.entered_people = self.entered_people + nb_people_entered
            self.talk("(5) Nb people entered %d " % nb_people_entered)
            
            # the elevator should be called again for the people that could enter
            if nb_people_entered <  len(new_people):
                self.talk("(5.1) Nb people entered not entered %d" % (nb_people_entered - len(new_people)))
                self.floors[self.current_floor].call_elevator(self)

        else:
            self.talk("(5) canno take more people, queued call")
            self.floors[self.current_floor].call_elevator(self)

        self.talk("(6) People in the elevator %d, current floor: %d \n\n" % (self.people.get_nb(), self.current_floor))

    # initializing the images of the elevator
    def init_img_elevator(self):
        # empty elevator
        img_empty = pygame.image.load(os.path.join('src','img', 'elevator_empty.png'))
        img_empty = pygame.transform.smoothscale(img_empty,(55, 95))
        # full elevator
        img_full = pygame.image.load(os.path.join('src','img', 'elevator_full.png'))
        img_full = pygame.transform.smoothscale(img_full,(55, 95))

        self.img_elevator = {self.IMG_EMPTY : img_empty,
                            self.IMG_FULL: img_full}

    # calculate the position of the elevator
    def calc_y_pos(self):
        if self.moving_counter > 0:
            self.pos_y = 22 + self.DISTANCE_FLOOR*self.current_floor + (1 - self.moving_counter/self.TIME_MOVING) * self.direction * self.DISTANCE_FLOOR 
    
    # draw the elevator on the screen
    def draw(self):
        if not self.emergency:
            self.serve()
            self.calc_y_pos()

        if(len(self.people) > 0):
            self.window.screen.blit(self.img_elevator[self.IMG_FULL], (self.pos_x, self.pos_y))
        else:
            self.window.screen.blit(self.img_elevator[self.IMG_EMPTY], (self.pos_x, self.pos_y))

        # Refreshing information (maybe put this code in state_changed)
        self.screen_info.refresh({"queue":self.queue,
                        "current_floor":self.current_floor,
                        "requested_floor":self.requested_floor,
                        "people":self.people,
                        "moving":self.direction,
                        "current_state": self.current_state,
                        "emergency": self.emergency})

    # use to print on the terminal the actions of the elevator
    def talk(self, comment, important=False):
        if self.talkative or important:
            print("Elevator: ", comment)
        
    def acceleration(self, mult):
        self.TIME_MOVING = self.TIME_MOVING * mult
        self.TIME_OPEN = self.TIME_OPEN * mult
