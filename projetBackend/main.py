import threading
import time
from elevator import Elevator
from floor import Floor

# creating floors
floors = []
floors.append(Floor(0))
floors.append(Floor(1))
floors.append(Floor(2))
# floors.append(Floor(3))
# print(floors[0].people_test)
# print(floors[1].people_test)
# print(floors[2].people_test)

elevator = Elevator(0, floors)
# create with other thread
def create_elevator():
    # global elevator
    elevator.start_serving()

def call1():
    # global elevator
    elevator.call(0)

t_elevator = threading.Thread(target=create_elevator)
t_elevator.start()

t_call1 = threading.Thread(target=call1)
t_call1.start()

time.sleep(2)
elevator.working = False

print("Entered: %d, Exit: %d"%(elevator.entered_people, elevator.exit_people))