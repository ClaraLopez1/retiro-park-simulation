import queue
import threading
from datetime import datetime

from Utils.database import log_boat_wait_time
from Utils.logger import log


class Boat:
    def __init__(self, boat_id):
        self.boat_id = boat_id
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


class BoatRental:
    def __init__(self, num_boats):
        self.boats = [Boat(i) for i in range(num_boats)]
        self.queue = queue.Queue()
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    def rent_boat(self, visitor_id):
        arrival_time = datetime.now()
        with self.condition:
            while True:
                for boat in self.boats:
                    if boat.rent(visitor_id):
                        assigned_time = datetime.now()
                        wait_duration = int((assigned_time - arrival_time).total_seconds())
                        log_boat_wait_time(visitor_id, arrival_time, assigned_time, wait_duration)
                        return boat


                log(f"⏳Visitor {visitor_id} is waiting for a boat.")
                self.queue.put(visitor_id)
                self.condition.wait()

    def return_boat(self, boat):
        with self.condition:
            boat.release()

            if not self.queue.empty():
                self.condition.notify()

    def notify_closure(self):
        with self.condition:
            self.condition.notify_all()