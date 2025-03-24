import random
import threading
import time
from Activities.activity import Activity
from Activities.Resources.boats import BoatRental
from Activities.Resources.bikes import BikeRental
from Activities.resource_activities import RentBoat, RentBike
from Activities.simple_activities import Walking, WatchingPerformance, TakingPhotos

class Visitor(threading.Thread):
    def __init__(self, visitor_id, park_activities):
        super().__init__()
        self.visitor_id = visitor_id
        self.park_activities = park_activities

    def run(self):
        while True:
            activity = random.choice(self.park_activities)

            print(f"Visitor {self.visitor_id} is starting: {activity.name}")

            activity.perform(self.visitor_id)
#test
print("hi")

if __name__ == "__main__":
    boat_rental = BoatRental(num_boats=2)
    bike_rental = BikeRental(num_bikes=2)

    park_activities = [
        Walking(),
        WatchingPerformance(),
        TakingPhotos(),
        RentBoat(boat_rental),
        RentBike(bike_rental)
    ]

    visitors = [Visitor(i, park_activities) for i in range(20)]

    for visitor in visitors:
        visitor.start()

    for visitor in visitors:
        visitor.join()