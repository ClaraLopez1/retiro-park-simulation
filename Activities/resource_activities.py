import time
from Activities import activity


class RentBoat(activity.Activity):
    def __init__(self, boat_rental):
        super().__init__("Renting a Boat", 10, 20)
        self.boat_rental = boat_rental

    def perform(self, visitor_id):
        print(f"Visitor {visitor_id} is trying to rent a boat.")
        boat = self.boat_rental.rent_boat(visitor_id)

        if boat:
            print(f"Visitor {visitor_id} is using Boat {boat.boat_id}.")
            time.sleep(self.duration)
            self.boat_rental.return_boat(boat)
            print(f"Visitor {visitor_id} finished kayaking.")

class RentBike(activity.Activity):
    def __init__(self, bike_rental):
        super().__init__("Renting a Bike", 5, 15)
        self.bike_rental = bike_rental

    def perform(self, visitor_id):
        print(f"Visitor {visitor_id} is trying to rent a bike.")
        bike = self.bike_rental.rent_bike(visitor_id)

        if bike:
            print(f"Visitor {visitor_id} is using Bike {bike.bike_id}.")
            time.sleep(self.duration)
            self.bike_rental.return_bike(bike)
            print(f"Visitor {visitor_id} finished biking.")
