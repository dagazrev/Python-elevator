class Person:
    def __init__(self, enter_floor, exit_floor, weight=60, gender=True, age=32):
        self.weight = weight
        self.gender = gender
        self.age = age
        self.enter_floor = enter_floor
        self.exit_floor = exit_floor

    def __str__(self):
        return "[Enter: %d, Exit: %d]"%(self.enter_floor, self.exit_floor)
