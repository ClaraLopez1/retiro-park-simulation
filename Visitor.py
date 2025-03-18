import random
import threading
import time
from Activities.activity import Activity
from Activities.Resources.boats import BoatRental
from Activities.resource_activities import RentBoat
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

            if isinstance(activity, RentBoat):
                activity.perform(self.visitor_id)
            else:
                activity.perform(self.visitor_id)

if __name__ == "__main__":
    boat_rental = BoatRental(num_boats=5)

    park_activities = [
        Walking(),
        WatchingPerformance(),
        TakingPhotos(),
        RentBoat(boat_rental)
    ]

    visitors = [Visitor(i, park_activities) for i in range(10)]

    for visitor in visitors:
        visitor.start()

    for visitor in visitors:
        visitor.join()
