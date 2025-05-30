import queue
import threading
from datetime import datetime

from Utils.database import log_bike_wait_time
from Utils.logger import log


class Bike:
    def __init__(self, bike_id):
        self.bike_id = bike_id
        self.lock = threading.Lock()
        self.is_rented = False

    def rent(self, visitor_id):
        with self.lock:
            if not self.is_rented:
                self.is_rented = True
                return True
            return False

    def release(self):
        with self.lock:
            self.is_rented = False

class BikeRental:
    def __init__(self, num_bikes):
        self.bikes = [Bike(i) for i in range(num_bikes)]
        self.queue = queue.Queue()
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock) #Allows threads to wait or be notified when resources are available

    def rent_bike(self, visitor_id):
        arrival_time = datetime.now()
        with self.condition:
            while True:
                for bike in self.bikes:
                    if bike.rent(visitor_id):
                        assigned_time = datetime.now()
                        wait_duration = int((assigned_time - arrival_time).total_seconds())
                        log_bike_wait_time(visitor_id, arrival_time, assigned_time, wait_duration)
                        return bike

                log(f"⏳Visitor {visitor_id} is waiting for a bike.")
                self.queue.put(visitor_id)
                self.condition.wait()

    def return_bike(self, bike):
        with self.condition:
            bike.release()

            if not self.queue.empty():
                self.condition.notify()

    def notify_closure(self):
        with self.condition:
            self.condition.notify_all()