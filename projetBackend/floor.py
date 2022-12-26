from people_group import PeopleGroup
from person import Person
import random

class Floor:
    def __init__(self, number):
        self.number = number

        # controlled
        # self.people_test = PeopleGroup([Person(number, ((number + 1) % 3) )])
        # print("Floor: %d, --> peson: %s" % (self.number, str(self.people_test.people[0])))

        # pseudo controlled
        # self.people_test = PeopleGroup([Person(number, 0), Person(number, 1), Person(number, 2)])

        # non controlled
        self.people_test = PeopleGroup([])
        for i in range(10):
            self.people_test.add_person(Person(self.number, random.randint(0,2)))

        print("Floor: %d"%self.number)
        print(self.people_test)

    def open_door(self, people_going_out):
        enter = self.people_test.people
        self.people_test.remove_all()
        print("Floor: %d nb people %d" % (self.number, len(self.people_test)))
        return PeopleGroup(enter)

    def close_door(self):
        pass