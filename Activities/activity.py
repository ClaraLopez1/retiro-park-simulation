import time
import random

from Utils.logger import log


class Activity:

    def __init__(self, name, min_duration, max_duration):
        self.name = name
        self.min_duration = min_duration
        self.max_duration = max_duration

    def perform(self, visitor_id):
        duration = random.randint(self.min_duration, self.max_duration)
        log(f"Visitor {visitor_id} is {self.name} for {duration} seconds")
        time.sleep(duration)
        log(f"Visitor {visitor_id} finished {self.name}.")
