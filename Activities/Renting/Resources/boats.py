import threading
from Utils.logger import log
from Utils.resource_queue import ResourceQueue


class Boat:
    def __init__(self, boat_id):
        self.boat_id = boat_id
        self.lock = threading.Lock()
        self.is_rented = False
        self.rented_by = None

    def rent(self, visitor_id):
        with self.lock:
            if not self.is_rented:
                self.is_rented = True
                self.rented_by = visitor_id
                return True
            return False

    def release(self):
        with self.lock:
            self.is_rented = False
            self.rented_by = None


class BoatRental:
    def __init__(self, num_boats):
        self.boats = [Boat(i) for i in range(num_boats)]
        self.lock = threading.Lock()
        
        # Use the generic ResourceQueue
        self.queue = ResourceQueue(
            resource_type="rental", 
            resource_name="boat", 
            capacity=num_boats
        )
    
    def rent_boat(self, visitor_id):
        """Try to rent a boat, join queue if none available"""
        # First try immediate access
        granted, position = self.queue.request_resource(visitor_id)
        
        if granted:
            # Find an available boat
            with self.lock:
                for boat in self.boats:
                    if boat.rent(visitor_id):
                        return boat, 0  # Return boat and wait time (0)
            
            # If we somehow got here, we were granted access but no boats available
            self.queue.release_resource(visitor_id)
            return None, 0
        
        # Return None and position if not granted
        return None, position
    
    def wait_for_boat(self, visitor_id, timeout=None):
        """Wait until a boat becomes available"""
        granted, wait_time = self.queue.wait_for_resource(visitor_id, timeout)
        
        if granted:
            # Find an available boat
            with self.lock:
                for boat in self.boats:
                    if boat.rent(visitor_id):
                        return boat, wait_time
            
            # If we somehow got here, we were granted access but no boats available
            self.queue.release_resource(visitor_id)
        
        return None, None
    
    def return_boat(self, boat, visitor_id):
        """Return a boat"""
        with self.lock:
            if boat.rented_by == visitor_id:
                boat.release()
                # Release resource in queue
                self.queue.release_resource(visitor_id)
                return True
            return False
    
    def get_queue_position(self, visitor_id):
        """Get position in queue"""
        return self.queue.get_position(visitor_id)
    
    def get_estimated_wait_time(self, visitor_id):
        """Estimate wait time"""
        return self.queue.get_estimated_wait_time(visitor_id, avg_use_time=15)
    
    def get_queue_length(self):
        """Get queue length"""
        return self.queue.get_queue_length()
    
    def notify_closure(self):
        """Notify all waiting threads when park is closing"""
        self.queue.notify_all()