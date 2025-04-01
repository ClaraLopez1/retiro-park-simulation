import random
import threading
import time

from Activities.Cafes.cafe import Cafe
from Activities.Cafes.visit_cafe import VisitCafe
from Activities.Renting.Resources.bikes import BikeRental
from Activities.Renting.Resources.boats import BoatRental
from Activities.Sports.sports_activities import SportActivity
from Activities.activity import Activity
from Activities.Renting.rent_boat import RentBoat
from Activities.Renting.rent_bike import RentBike
from Activities.simple_activities import Walking, WatchingPerformance, TakingPhotos, Running

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
    boat_rental = BoatRental(num_boats=5)
    bike_rental = BikeRental(num_bikes=7)
    star_cafe = Cafe("StarCafe", num_baristas=2)
    retiro_bistro = Cafe("RetiroBistro", num_baristas=3)
    football7v7 = SportActivity("Football 7v7", 14, min_duration=10, max_duration=20)
    football13v13 = SportActivity("Football 13v13", 26, min_duration=15, max_duration=30)
    padel = SportActivity("Padel", 4, min_duration=5, max_duration=10)
    tennis = SportActivity("Tennis", 2, min_duration=3, max_duration=7)

    park_activities = [
        Walking(),
        WatchingPerformance(),
        TakingPhotos(),
        Running(),
        RentBoat(boat_rental),
        RentBike(bike_rental),
        VisitCafe(star_cafe),
        VisitCafe(retiro_bistro),
        football7v7,
        football13v13,
        padel,
        tennis
    ]

    visitors = [Visitor(i, park_activities) for i in range(50)]

    for visitor in visitors:
        visitor.start()

    for visitor in visitors:
        visitor.join()