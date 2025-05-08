from UI.park_map import get_activity_coord
from Activities.activity import Activity
from Utils.logger import log
import time

class RentBoat(Activity):
    def __init__(self, boat_rental):
        super().__init__("renting a Boat", 2, 10)
        self.boat_rental = boat_rental
        self.coords = get_activity_coord(self.name)

    def perform(self, visitor_id):
        boat = self.boat_rental.rent_boat(visitor_id)
        if boat:
            duration = self.duration
            log(f"🚣 Visitor {visitor_id} is using Boat {duration}.")
            time.sleep(duration)
            self.boat_rental.return_boat(boat)
            log(f"🚣 Visitor {visitor_id} finished kayaking.")
