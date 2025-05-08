import time
import random
from Activities.activity import Activity
from Utils.logger import log
from UI.park_map import get_activity_coord


class RentBike(Activity):
    def __init__(self, bike_rental):
        super().__init__("Rent a Bike", min_duration=5, max_duration=15)
        self.bike_rental = bike_rental
        self.coords = get_activity_coord(self.name)


    def perform(self, visitor_id):
        # Try to rent a bike immediately
        bike, wait_time = self.bike_rental.rent_bike(visitor_id)
        
        if not bike:
            # Check current queue length and estimated wait
            queue_length = self.bike_rental.get_queue_length()
            estimated_wait = self.bike_rental.get_estimated_wait_time(visitor_id)
            
            # Visitor might decide not to wait if queue is too long
            if queue_length > 3 and random.random() < 0.3:
                log(f"Visitor {visitor_id} decided not to wait in bike queue (length: {queue_length})")
                self.bike_rental.queue.leave_queue(visitor_id)
                return
            
            log(f"Visitor {visitor_id} waiting for bike. Estimated wait: {estimated_wait:.1f}s")
            
            # Wait for a bike (timeout after 30 seconds)
            bike, wait_time = self.bike_rental.wait_for_bike(visitor_id, timeout=30)
            
            # If still no bike (timeout), give up
            if not bike:
                log(f"Visitor {visitor_id} gave up waiting for a bike")
                return
        
        # Successfully got a bike, now use it
        try:
            # Determine rental duration
            duration = random.randint(self.min_duration, self.max_duration)
            log(f"Visitor {visitor_id} is riding bike {bike.bike_id} for {duration} minutes")
            
            # Simulate the activity
            time.sleep(duration * 0.1)  # Scaled time
            
        finally:
            # Always return the bike, even if interrupted
            self.bike_rental.return_bike(bike, visitor_id)
