import time
from Activities import activity
from Utils.logger import log
from UI.park_map import get_activity_coord


class RentBike(activity.Activity):
    def __init__(self, bike_rental):
        super().__init__("Renting a Bike", 5, 15)
        self.bike_rental = bike_rental
        self.coords = get_activity_coord(self.name)


    def perform(self, visitor_id):
        log(f"Visitor {visitor_id} is traveling to {self.coords}  for {self.name}")
        bike = self.bike_rental.rent_bike(visitor_id)
        if bike:
            log(f"Visitor {visitor_id} is using Bike {bike.bike_id}.")
            time.sleep(self.duration)
            self.bike_rental.return_bike(bike)
            log(f"Visitor {visitor_id} finished biking.")
