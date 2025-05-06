from datetime import datetime
from UI.gui import start_gui
from Activities.Cafes.Menu.MenuItem import MenuItem
from Activities.Cafes.cafe import Cafe
from Activities.Cafes.visit_cafe import VisitCafe
from Activities.Renting.Resources.bikes import BikeRental
from Activities.Renting.Resources.boats import BoatRental
from Activities.Renting.rent_bike import RentBike
from Activities.Renting.rent_boat import RentBoat
from Activities.Sports.sports_activities import SportActivity, SportCourt
from Activities.simple_activities import Walking, WatchingPerformance, TakingPhotos, Running, PalacioCristal, \
    AngelCaido, PalacioVelazquez
from Time_manager import TimeManager
from Visitor import Visitor


class RetiroPark:
    def __init__(self, num_visitors):
        self.activities = self._create_activities()
        self.time_manager = TimeManager(
            time_scale=0.2,
        )
        self.visitors = [Visitor(i, self.activities) for i in range(num_visitors)]

        for visitor in self.visitors:
            visitor.set_time_manager(self.time_manager)

    def _create_activities(self):
        boat_rental = BoatRental(num_boats=5)
        bike_rental = BikeRental(num_bikes=7)

        menu_star = [
            MenuItem("Latte", 3.50, "Espresso con leche vaporizada"),
            MenuItem("Croissant", 2.00, "Croissant de manteca recién horneado"),
            MenuItem("Brownie", 2.80, "Brownie de chocolate con nueces"),
        ]

        menu_bistro = [
            MenuItem("Café solo", 1.80, "Café negro tradicional"),
            MenuItem("Tostadas con mermelada", 2.20, "Pan tostado con mermelada de frutilla"),
            MenuItem("Té verde", 2.00, "Té verde orgánico"),
        ]

        star_cafe = Cafe("StarCafe", num_baristas=10, menu_items=menu_star)
        retiro_bistro = Cafe("RetiroBistro", num_baristas=3, menu_items=menu_bistro)

        return [
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
            SportActivity("Football 7v7", 14, SportCourt("Football 7v7"), min_duration=10, max_duration=20),
            SportActivity("Padel", 4, SportCourt("Padel"), min_duration=5, max_duration=10),
            SportActivity("Tennis", 2, SportCourt("Tennis"), min_duration=3, max_duration=7),
        ]

    def start(self):
        self.time_manager.start()
        for visitor in self.visitors:
            visitor.start()
        start_gui(self.visitors, self.time_manager)


if __name__ == "__main__":
    park = RetiroPark(num_visitors=50)
    park.start()
