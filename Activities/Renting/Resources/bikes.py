import threading
from Utils.logger import log
from Utils.resource_queue import ResourceQueue


class Bike:
    def __init__(self, bike_id):
        self.bike_id = bike_id
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

class BikeRental:
    def __init__(self, num_bikes):
        self.bikes = [Bike(i) for i in range(num_bikes)]
        self.lock = threading.Lock()
        
        # Use the generic ResourceQueue
        self.queue = ResourceQueue(
            resource_type="rental", 
            resource_name="bike", 
            capacity=num_bikes
        )
    
    def rent_bike(self, visitor_id):
        """Try to rent a bike, join queue if none available"""
        # First try immediate access
        granted, position = self.queue.request_resource(visitor_id)
        
        if granted:
            # Find an available bike
            with self.lock:
                for bike in self.bikes:
                    if bike.rent(visitor_id):
                        return bike, 0  # Return bike and wait time (0)
            
            # If we somehow got here, we were granted access but no bikes available
            # This should not happen but let's be safe
            self.queue.release_resource(visitor_id)
            return None, 0
        
        # Return None and position if not granted
        return None, position
    
    def wait_for_bike(self, visitor_id, timeout=None):
        """Wait until a bike becomes available"""
        granted, wait_time = self.queue.wait_for_resource(visitor_id, timeout)
        
        if granted:
            # Find an available bike
            with self.lock:
                for bike in self.bikes:
                    if bike.rent(visitor_id):
                        return bike, wait_time
            
            # If we somehow got here, we were granted access but no bikes available
            self.queue.release_resource(visitor_id)
        
        return None, None
    
    def return_bike(self, bike, visitor_id):
        """Return a bike"""
        with self.lock:
            if bike.rented_by == visitor_id:
                bike.release()
                # Release resource in queue
                self.queue.release_resource(visitor_id)
                return True
            return False
    
    def get_queue_position(self, visitor_id):
        """Get position in queue"""
        return self.queue.get_position(visitor_id)
    
    def get_estimated_wait_time(self, visitor_id):
        """Estimate wait time"""
        return self.queue.get_estimated_wait_time(visitor_id, avg_use_time=10)
    
    def get_queue_length(self):
        """Get queue length"""
        return self.queue.get_queue_length()
    
    def notify_closure(self):
        """Notify all waiting threads when park is closing"""
        self.queue.notify_all()