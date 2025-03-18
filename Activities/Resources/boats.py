import queue
import threading
import time
import random

class Boat:
    def __init__(self, boat_id):
        self.boat_id = boat_id
        self.lock = threading.Lock()
        self.is_rented = False

    def rent(self, visitor_id):
        with self.lock:
            if not self.is_rented:
                self.is_rented = True
                print(f"Visitor {visitor_id} rented Boat {self.boat_id}.")
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
        with self.condition:
            while True:
                for boat in self.boats:
                    if boat.rent(visitor_id):
                        return boat


                print(f"Visitor {visitor_id} is waiting for a boat.")
                self.queue.put(visitor_id)
                self.condition.wait()

    def return_boat(self, boat):
        with self.condition:
            boat.release()
            print(f"Boat {boat.boat_id} is now available.")

            if not self.queue.empty():
                next_visitor = self.queue.get()
                print(f"Visitor {next_visitor}, a boat is now available!")
                self.condition.notify()
