import random
import threading
from Activities.Cafes.cafe import Cafe
from Activities.Cafes.visit_cafe import VisitCafe
from Activities.Renting.Resources.bikes import BikeRental
from Activities.Renting.Resources.boats import BoatRental
from Activities.Sports.sports_activities import SportActivity, SportCourt
from Activities.activity import Activity
from Activities.Renting.rent_boat import RentBoat
from Activities.Renting.rent_bike import RentBike
from Activities.simple_activities import Walking, WatchingPerformance, TakingPhotos, Running, PalacioCristal, \
    AngelCaido, PalacioVelazquez
from logger import log
from gui import start_gui
import random
import threading
import time
from logger import log
from park_map import get_activity_coord


class Visitor(threading.Thread):
    def __init__(self, visitor_id, park_activities):
        super().__init__()
        self.visitor_id = visitor_id
        self.park_activities = park_activities
        self.coords = (10, 10)  # Start with a default coordinate

    def smooth_move(self, start_coords, end_coords, steps=20, step_delay=0.05):
        """Smoothly move from start_coords to end_coords over a number of steps."""
        sx, sy = start_coords
        ex, ey = end_coords
        dx = (ex - sx) / steps
        dy = (ey - sy) / steps
        for i in range(steps):
            # Update self.coords gradually
            new_x = sx + dx * (i + 1)
            new_y = sy + dy * (i + 1)
            self.coords = (new_x, new_y)
            time.sleep(step_delay)

    def run(self):
        while True:
            activity = random.choice(self.park_activities)
            target_coords = get_activity_coord(activity.name)
            if self.coords != target_coords:
                log(f"Visitor {self.visitor_id} moving from {self.coords} to {target_coords} for {activity.name}")
                self.smooth_move(self.coords, target_coords)
            log(f"Visitor {self.visitor_id} is starting: {activity.name} at {self.coords}")
            activity.perform(self.visitor_id)


if __name__ == "__main__":
    boat_rental = BoatRental(num_boats=5)
    bike_rental = BikeRental(num_bikes=7)
    star_cafe = Cafe("StarCafe", num_baristas=2)
    retiro_bistro = Cafe("RetiroBistro", num_baristas=3)
    football7v7 = SportActivity("Football 7v7", 14, SportCourt("Football 7v7"), min_duration=10, max_duration=20)
    # football13v13 = SportActivity("Football 13v13", 26, min_duration=15, max_duration=30)
    padel = SportActivity("Padel", 4, SportCourt("Padel"), min_duration=5, max_duration=10)
    tennis = SportActivity("Tennis", 2, SportCourt("Tennis"),min_duration=3, max_duration=7)

    park_activities = [
        Walking(),
        WatchingPerformance(),
        TakingPhotos(),
        Running(),
        PalacioCristal(),
        AngelCaido(),
        PalacioVelazquez(),
        RentBoat(boat_rental),
        RentBike(bike_rental),
        VisitCafe(star_cafe),
        VisitCafe(retiro_bistro),
        football7v7,
        # football13v13,
        padel,
        tennis
    ]

    visitors = [Visitor(i, park_activities) for i in range(50)]
    for visitor in visitors:
        visitor.start()

    start_gui(visitors)
