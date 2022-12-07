import time
from people_group import PeopleGroup


class Elevator:
    def __init__(self, c_floor, floors):
        self.c_floor = c_floor
        self.floors = floors
        self.queue = []
        self.people_group = PeopleGroup()
        self.charge_max = 1900
        self.moving_time = 1
        self.wait_time = 1
        self.working = True

        self.entered_people = 0
        self.exit_people = 0
  

    def call(self, floor):
        print("Elevator: floor called %d " % floor)
        self.queue.append(floor)

    def request_inside(self, floor):
        print("Elevator: internal call %d " % floor)
        self.queue.append(floor)

    def start_serving(self):
        print("Elevator: start serving\n")
        self.__serve()

    # this method will be in charge of the service of the elevetor
    # will be always waiting for a button to be pressed to go to a floor
    # this is like the control panel of the elevator
    def __serve(self):
        while self.working:
            if len(self.queue) > 0:
                d_floor = self.queue.pop(0)

                print("Elevator: (1) call foun in floor nro: %d" % d_floor)
                # Request floor is equal to the elevator's floor
                if self.c_floor == d_floor:
                    #open the door, wait for the person to go inside/outside, then close the door
                    print("Elevator: called from the same floor")
                    self.open_door()

                # Request floor is other than the elevator's floor
                else:
                    direction = self.direction(d_floor)
                    while self.c_floor != d_floor:
                        print("Elevator: (2) moving to %d, current floor: %d" % (d_floor,self.c_floor))

                        # time between floors
                        # time.sleep(self.moving_time)

                        # Here you check if the current floor was asked
                        # if so, open the door, wait for the person to go inside/outside, then close the door
                        if self.c_floor in self.queue:
                            print("Elevator: (2.2) picking up someone in floor: %d" % self.c_floor)
                            self.open_door()
                            # self.queue = list(filter((self.c_floor).__ne__, self.queue))
                            
                        self.c_floor = self.c_floor + direction
                    #open the door, wait for the person to go inside/outside, then close the door
                    print("Elevator: Arrived to destination floor %d" % (self.c_floor))

                    self.open_door()


    def direction(self, d_floor):
        res = self.c_floor - d_floor
        if res < 0:
            return 1
        else :
            return -1


    # people_going_out: list with the pople that is going out
    def open_door(self):
        print(self.queue)
        print("Elevator: (3) opening the door on floor %d" % self.c_floor)
        # removing people going out people going out
        people_going_out = self.people_group.get_exit_floor(self.c_floor)
        self.people_group.remove_sub_group(people_going_out)
        self.exit_people = self.exit_people + people_going_out.get_nb()
        self.queue = list(filter((self.c_floor).__ne__, self.queue))

        print("Elevator: (4) Nb people went out %d " % people_going_out.get_nb())


        # oppening the door in the floor and letting the people to go out
        # also obtaining the people that is entering
        new_people = self.floors[self.c_floor].open_door(people_going_out)
        self.people_group.join(new_people)
        # print("Elevator: PEO: ", str(self.people_group.get_exit_floor(self.c_floor)))
        # self.people_group.remove_sub_group(self.people_group.get_exit_floor(self.c_floor))
        self.entered_people = self.entered_people + new_people.get_nb()
        print("Elevator: (5) Nb people entered %d " % new_people.get_nb())
        print("Elevator: (6) Total people %d, cf: %d \n\n" % (self.people_group.get_nb(), self.c_floor))

        # internal command
        for p in new_people:
            # if p.exit_floor != self.c_floor:
            self.request_inside(p.exit_floor)


    # # people_going_out: list with the pople that is going out
    # def open_door(self, people_group, mode):
    #     print("Oppening the door, nb of people = ", people_group.get_nb(), " entering : ", mode)

    #   # people entering
    #   if mode:
    #     self.people_group.remove(people_group)


    #   new_people = self.floors[self.c_floor].open_door(people_going_out)
    #   print("New people entering = ", new_people.get_nb())

    #   # wait some time while the animation of the doors and the people is running
    #   # check the current weight of the elevator
    #   while PeopleGroup.join(self.people_group, new_people).get_weight() > self.charge_max:
    #     # over weight 
    #     new_people = self.floors[self.c_floor].over_weight():

    #   # new group of people in the elevator (can be an empty group)
    #   self.people_group.join(new_people) 

    #   # the thread will come when the people finish to enter or going out
    #   self.floors[self.c_floor].close_door()
    #   print("the door is closed = ", new_people.get_nb())



