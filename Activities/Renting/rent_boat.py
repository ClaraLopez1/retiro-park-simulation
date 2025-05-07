import time
import random
from Activities.activity import Activity
from Utils.logger import log

class RentBoat(Activity):
    def __init__(self, boat_rental):
        super().__init__("Rent a Boat", min_duration=10, max_duration=20)
        self.boat_rental = boat_rental
    
    def perform(self, visitor_id):
        # Try to rent a boat immediately
        boat, wait_time = self.boat_rental.rent_boat(visitor_id)
        
        if not boat:
            # Check current queue length and estimated wait
            queue_length = self.boat_rental.get_queue_length()
            estimated_wait = self.boat_rental.get_estimated_wait_time(visitor_id)
            
            # Visitor might decide not to wait if queue is too long
            if queue_length > 2 and random.random() < 0.4:
                log(f"Visitor {visitor_id} decided not to wait in boat queue (length: {queue_length})")
                self.boat_rental.queue.leave_queue(visitor_id)
                return
            
            log(f"Visitor {visitor_id} waiting for boat. Estimated wait: {estimated_wait:.1f}s")
            
            # Wait for a boat (timeout after 40 seconds - boats are worth waiting for longer)
            boat, wait_time = self.boat_rental.wait_for_boat(visitor_id, timeout=40)
            
            # If still no boat (timeout), give up
            if not boat:
                log(f"Visitor {visitor_id} gave up waiting for a boat")
                return
        
        # Successfully got a boat, now use it
        try:
            # Determine rental duration
            duration = random.randint(self.min_duration, self.max_duration)
            log(f"Visitor {visitor_id} is boating with boat {boat.boat_id} for {duration} minutes")
            
            # Simulate the activity
            time.sleep(duration * 0.1)  # Scaled time
            
        finally:
            # Always return the boat, even if interrupted
            self.boat_rental.return_boat(boat, visitor_id)
