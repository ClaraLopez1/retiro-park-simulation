import threading
import time
from collections import deque
from Utils.logger import log

class ResourceQueue:
    """
    Can be used by any activity type that requires queuing.
    """
    def __init__(self, resource_type, resource_name, capacity=None):
        """
        Initialize a resource queue.
        
        Args:
            resource_type (str): General type (e.g., 'sport', 'cafe', 'rental')
            resource_name (str): Specific name (e.g., 'tennis', 'StarCafe', 'bike')
            capacity (int): Maximum number of concurrent users (None for unlimited)
        """
        # Resource identification
        self.resource_type = resource_type
        self.resource_name = resource_name
        
        # Resource capacity
        self.capacity = capacity
        self.current_users = 0
        
        # Queue data structure
        self.queue = deque()
        
        # Timestamp tracking
        self.join_times = {}
        
        # Thread synchronization
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        
        log(f"Created {resource_type} queue for {resource_name} with capacity {capacity}")
    
    def request_resource(self, visitor_id):
        """
        Request access to the resource. Either grants immediate access or queues.
        
        Returns:
            tuple: (granted, position) - whether access was granted immediately and position if queued
        """
        with self.lock:
            # Check if capacity available
            if self.capacity is None or self.current_users < self.capacity:
                self.current_users += 1
                log(f"Visitor {visitor_id} granted immediate access to {self.resource_name}")
                return True, 0
            
            # No capacity, add to queue
            self.queue.append(visitor_id)
            self.join_times[visitor_id] = time.time()
            position = len(self.queue)
            
            log(f"Visitor {visitor_id} queued for {self.resource_name} at position {position}")
            return False, position
    
    def wait_for_resource(self, visitor_id, timeout=None):
        """
        Wait until resource becomes available.
        
        Args:
            visitor_id (int): ID of waiting visitor
            timeout (float): Maximum wait time in seconds (None for indefinite)
            
        Returns:
            tuple: (access_granted, wait_time) or (False, None) if timeout
        """
        start_time = time.time()
        
        while True:
            # Check for timeout
            if timeout and time.time() - start_time > timeout:
                self.leave_queue(visitor_id)
                log(f"Visitor {visitor_id} timed out waiting for {self.resource_name}")
                return False, None
            
            with self.lock:
                # Check if we're first in queue
                if self.queue and self.queue[0] == visitor_id:
                    # Check if capacity available
                    if self.capacity is None or self.current_users < self.capacity:
                        # Remove from queue
                        self.queue.popleft()
                        wait_time = time.time() - self.join_times.pop(visitor_id)
                        
                        # Grant access
                        self.current_users += 1
                        
                        log(f"Visitor {visitor_id} granted access to {self.resource_name} after {wait_time:.1f}s wait")
                        return True, wait_time
                
                # Wait for notification of change
                self.condition.wait(timeout=5 if timeout is None else min(5, timeout))
            
            # Check if visitor left the queue somehow (e.g., park closing)
            with self.lock:
                if visitor_id not in [v for v in self.queue]:
                    return False, None
    
    def release_resource(self, visitor_id):
        """
        Release a resource after use.
        
        Args:
            visitor_id (int): ID of visitor releasing resource
        """
        with self.lock:
            self.current_users -= 1
            log(f"Visitor {visitor_id} released {self.resource_name}")
            
            # Notify waiting visitors
            self.condition.notify_all()
    
    def leave_queue(self, visitor_id):
        """Allow visitor to abandon queue"""
        with self.lock:
            try:
                self.queue.remove(visitor_id)
                if visitor_id in self.join_times:
                    del self.join_times[visitor_id]
                
                log(f"Visitor {visitor_id} left queue for {self.resource_name}")
                return True
            except ValueError:
                return False
    
    def get_position(self, visitor_id):
        """Get visitor's position in queue (1-indexed)"""
        with self.lock:
            try:
                return self.queue.index(visitor_id) + 1
            except ValueError:
                return None
    
    def get_estimated_wait_time(self, visitor_id, avg_use_time=10):
        """Estimate wait time based on position and average use time"""
        position = self.get_position(visitor_id)
        if position is None:
            return None
        
        with self.lock:
            # Formula: (position / capacity) * average_use_time
            capacity = max(1, self.capacity if self.capacity else 1)
            return (position / capacity) * avg_use_time
    
    def get_queue_length(self):
        """Get current queue length"""
        with self.lock:
            return len(self.queue)
    
    def notify_all(self):
        """Notify all waiting threads (e.g., for park closure)"""
        with self.lock:
            self.condition.notify_all()