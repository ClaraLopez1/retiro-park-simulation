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
from time_manager import TimeManager
from datetime import datetime


class Visitor(threading.Thread):
    def __init__(self, visitor_id, park_activities, time_manager):
        super().__init__()
        self.visitor_id = visitor_id
        self.park_activities = park_activities
        self.coords = (10, 10)  # Start with a default coordinate
        self.time_manager = time_manager
        self.preferences = self._generate_preferences()
        self.is_leaving = False
        self.exit_coords = (10, 10)  # Default exit coordinates
        self.has_left_park = False  # Track if visitor has completely left the park
        self.is_active = True  # Track if the visitor thread is active
        
    def _generate_preferences(self):
        """Generate visitor preferences based on time of day."""
        return {
            'morning': {
                'cafe': random.uniform(0.3, 0.7),
                'sports': random.uniform(0.6, 0.9),
                'kayak': random.uniform(0.4, 0.8),
                'walking': random.uniform(0.7, 1.0)
            },
            'afternoon': {
                'cafe': random.uniform(0.5, 0.8),
                'sports': random.uniform(0.4, 0.7),
                'kayak': random.uniform(0.6, 0.9),
                'walking': random.uniform(0.5, 0.8)
            },
            'evening': {
                'cafe': random.uniform(0.7, 1.0),
                'sports': random.uniform(0.2, 0.5),
                'kayak': random.uniform(0.3, 0.6),
                'walking': random.uniform(0.6, 0.9)
            },
            'night': {
                'cafe': random.uniform(0.1, 0.3),
                'sports': random.uniform(0.1, 0.3),
                'kayak': random.uniform(0.1, 0.3),
                'walking': random.uniform(0.1, 0.3)
            }
        }

    def smooth_move(self, start_coords, end_coords, steps=20, step_delay=0.05):
        """Smoothly move from start_coords to end_coords over a number of steps."""
        sx, sy = start_coords
        ex, ey = end_coords
        dx = (ex - sx) / steps
        dy = (ey - sy) / steps
        for i in range(steps):
            if not self.time_manager.is_park_open() and not self.is_leaving:
                log(f"Visitor {self.visitor_id} leaving the park as it's closing time")
                self.is_leaving = True
                return False
            # Update self.coords gradually
            new_x = sx + dx * (i + 1)
            new_y = sy + dy * (i + 1)
            self.coords = (new_x, new_y)
            time.sleep(step_delay)
        return True

    def _select_activity(self):
        """Select an activity based on time of day and preferences."""
        # Check if park is closing soon
        if self.time_manager.is_park_closing_soon(minutes=30) and not self.is_leaving:
            log(f"Visitor {self.visitor_id} preparing to leave as park is closing soon")
            self.is_leaving = True
            return None
            
        time_of_day = self.time_manager.get_time_of_day()
        available_activities = []
        
        for activity in self.park_activities:
            # Skip activities if park is closing soon
            if not self.time_manager.is_park_open() and not self.is_leaving:
                continue
                
            # Check if activity is appropriate for current time
            if isinstance(activity, (VisitCafe, Cafe)) and time_of_day == 'morning':
                continue  # Skip cafes in the morning
                
            if isinstance(activity, (SportActivity, RentBoat, RentBike)) and time_of_day == 'evening':
                continue  # Skip sports and rentals in the evening
                
            # Calculate preference score
            activity_type = activity.__class__.__name__.lower()
            preference_score = self.preferences[time_of_day].get(activity_type, 0.5)
            
            if random.random() < preference_score:
                available_activities.append(activity)
                
        return random.choice(available_activities) if available_activities else None

    def run(self):
        # Wait until park is open before starting
        while not self.time_manager.is_park_open() and not self.has_left_park and self.is_active:
            time.sleep(0.1)
            
        while self.time_manager.is_park_open() or self.is_leaving:
            # Check if it's 10:00 PM - time to leave the park
            current_time = self.time_manager.get_current_time()
            if current_time.hour == 22 and current_time.minute == 0 and not self.is_leaving:
                log(f"Visitor {self.visitor_id} preparing to leave as it's 10:00 PM")
                self.is_leaving = True
                
            # If leaving, move to exit
            if self.is_leaving:
                if self.coords != self.exit_coords:
                    log(f"Visitor {self.visitor_id} moving to exit at {self.exit_coords}")
                    self.smooth_move(self.coords, self.exit_coords)
                else:
                    log(f"Visitor {self.visitor_id} has left the park")
                    self.has_left_park = True
                    break
                    
            activity = self._select_activity()
            if not activity:
                if not self.is_leaving:
                    log(f"Visitor {self.visitor_id} cannot find suitable activity, leaving park")
                    self.is_leaving = True
                continue
                
            target_coords = get_activity_coord(activity.name)
            if self.coords != target_coords:
                log(f"Visitor {self.visitor_id} moving from {self.coords} to {target_coords} for {activity.name}")
                if not self.smooth_move(self.coords, target_coords):
                    continue
                    
            log(f"Visitor {self.visitor_id} is starting: {activity.name} at {self.coords}")
            activity.perform(self.visitor_id)
            
        # If we've left the park, wait until the next day
        if self.has_left_park:
            # Wait until the park opens again
            while not self.time_manager.is_park_open() and self.is_active:
                time.sleep(0.1)
                
            # Only create a new visitor if we're still active
            if self.is_active:
                # Reset leaving state for the new day
                self.is_leaving = False
                self.has_left_park = False
                log(f"Visitor {self.visitor_id} returning to the park for a new day")
                
                # Start a new thread for the next day
                new_visitor = Visitor(self.visitor_id, self.park_activities, self.time_manager)
                new_visitor.start()
                
                # End this thread
                self.is_active = False
                log(f"Visitor {self.visitor_id} thread ending, new visitor created for next day")
    
    def stop(self):
        """Stop the visitor thread."""
        self.is_active = False
        log(f"Visitor {self.visitor_id} stopping")


if __name__ == "__main__":
    # Initialize time manager with a reasonable time scale
    start_time = datetime.now().replace(hour=5, minute=55, second=0, microsecond=0)
    time_manager = TimeManager(
        start_time=start_time,
        time_scale=0.2,  # 0.2 real seconds = 1 simulation minute (5 simulation minutes per real second)
        start_day="Monday"
    )
    
    # Start time manager
    time_manager.start()
    
    # Initialize activities
    boat_rental = BoatRental(num_boats=5)
    bike_rental = BikeRental(num_bikes=7)
    star_cafe = Cafe("StarCafe", num_baristas=2)
    retiro_bistro = Cafe("RetiroBistro", num_baristas=3)
    football7v7 = SportActivity("Football 7v7", 14, SportCourt("Football 7v7"), min_duration=10, max_duration=20)
    # football13v13 = SportActivity("Football 13v13", 26, min_duration=15, max_duration=30)
    padel = SportActivity("Padel", 4, SportCourt("Padel"), min_duration=5, max_duration=10)
    tennis = SportActivity("Tennis", 2, SportCourt("Tennis"), min_duration=3, max_duration=7)

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

    visitors = [Visitor(i, park_activities, time_manager) for i in range(50)]
    for visitor in visitors:
        visitor.start()

    start_gui(visitors, time_manager)
    
    # Stop time manager when simulation ends
    time_manager.stop()
    
    # Clean up visitor threads
    for visitor in visitors:
        visitor.stop()
        visitor.join()
