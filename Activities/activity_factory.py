from Activities.Renting.Resources.bikes import BikeRental
from Activities.Renting.Resources.boats import BoatRental
from Activities.Renting.rent_bike import RentBike
from Activities.Renting.rent_boat import RentBoat
from Activities.Cafes.Menu.MenuItem import MenuItem
from Activities.Cafes.cafe import Cafe
from Activities.Cafes.visit_cafe import VisitCafe
from Activities.Sports.sports_activities import SportActivity, SportCourt
from Activities.simple_activities import *

class ActivityFactory:
    def __init__(self):
        self.boat_rental = BoatRental(num_boats=6)
        self.bike_rental = BikeRental(num_bikes=7)

    def create_all(self):
        activities = []

        # Simple activities
        activities += [
            Walking(),
            WatchingPerformance(),
            TakingPhotos(),
            Running(),
            PalacioCristal(),
            AngelCaido(),
            PalacioVelazquez()
        ]

        # Rentals
        activities.append(RentBoat(self.boat_rental))
        activities.append(RentBike(self.bike_rental))

        # Cafes
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

        star_cafe = Cafe("StarCafe", num_baristas=2, menu_items=menu_star)
        retiro_bistro = Cafe("RetiroBistro", num_baristas=1, menu_items=menu_bistro)

        activities.append(VisitCafe(star_cafe))
        activities.append(VisitCafe(retiro_bistro))

        # Sports
        activities.append(SportActivity("Football 7v7", 14, SportCourt("Football 7v7"), min_duration=5, max_duration=10))
        activities.append(SportActivity("Padel", 4, SportCourt("Padel"), min_duration=2, max_duration=5))
        activities.append(SportActivity("Tennis", 2, SportCourt("Tennis"), min_duration=3, max_duration=5))

        return activities
