from people_group import PeopleGroup
from person import Person
import random

class Floor:
    def __init__(self, window, number):
        self.window = window
        self.number = number

        self.x = 275
        self.y = 50 + self.number*94
        self.people = PeopleGroup([])

        # this function should be in the main with an external thread inside of a infinite boucle
        # self.create_people()

    # create from 0 up to 3 people ramdomly and add to the people group
    # the people is create only if there is not people on the floor, otherwise no body is created
    def create_people(self):
        if len(self.people) == 0:
            nb_people = random.randint(0,13)
            for i in range(nb_people):
                person = Person(self.number, random.randint(0,7),  weight=random.randint(45,90), gender=bool(random.getrandbits(1)) )
                # person = Person(self.number, self.number,  weight=random.randint(45,90), gender=bool(random.getrandbits(1)) )

                self.people.add_person(person)

    def open_door(self, people_going_out):
        enter = self.people.people
        self.people.remove_all()
        print("Floor: %d nb people %d" % (self.number, len(self.people)))
        return PeopleGroup(enter)

    def over_weight(self, people):
        self.people.join(people)

    def close_door(self):
        pass

    def draw(self):
        p_i = 0
        p_space = 25
        for p in self.people:
            self.window.screen.blit(p.img, (self.x-p_i*p_space, self.y))
            p_i = p_i + 1

    def has_people(self):
        return len(self.people) > 0




