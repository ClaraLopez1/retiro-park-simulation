import time
from Activities import activity




class RentBike(activity.Activity):
    def __init__(self, bike_rental):
        super().__init__("Renting a Bike", 5, 15)
        self.bike_rental = bike_rental

    def perform(self, visitor_id):
        bike = self.bike_rental.rent_bike(visitor_id)

        if bike:
            print(f"Visitor {visitor_id} is using Bike {bike.bike_id}.")
            time.sleep(self.duration)
            self.bike_rental.return_bike(bike)
            print(f"Visitor {visitor_id} finished biking.")
