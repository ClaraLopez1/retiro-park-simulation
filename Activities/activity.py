import time
import random

from Utils.logger import log


class Activity:

    def __init__(self, name, min_duration, max_duration):
        self.name = name
        self.duration = random.randint(min_duration, max_duration)

    def perform(self, visitor_id):
        log(f"Visitor {visitor_id} is {self.name} for {self.duration} seconds")
        time.sleep(self.duration)
        log(f"Visitor {visitor_id} finished {self.name}.")
