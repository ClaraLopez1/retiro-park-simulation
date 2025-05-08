import threading
import time
import random
from Activities.activity import Activity
from Utils.logger import log
from UI.park_map import get_activity_coord
from queue import Queue
from Utils.resource_queue import ResourceQueue

from Utils.database import log_sport_game

class SportCourt:
    def __init__(self, name, capacity=None):
        self.name = name
        self.queue = ResourceQueue(
            resource_type="sport",
            resource_name=name,
            capacity=capacity
        )


class SportActivity(Activity):
    def __init__(self, name, required_people, court, min_duration=2, max_duration=5):
        super().__init__(name, min_duration=min_duration, max_duration=max_duration)
        self.required_people = required_people
        self.court = court
        self.condition = threading.Condition()

    def perform(self, visitor_id):
        # Request access to the court
        granted, position = self.court.queue.request_resource(visitor_id)

        if not granted:
            # Wait in queue if court is busy
            estimated_wait = self.court.queue.get_estimated_wait_time(visitor_id)
            log(f"Visitor {visitor_id} waiting for {self.name}. Position: {position}, Est. wait: {estimated_wait:.1f}s")

            # Visitor might decide not to wait if queue is too long
            if position > 2 and random.random() < 0.3:
                log(f"Visitor {visitor_id} decided not to wait for {self.name}")
                self.court.queue.leave_queue(visitor_id)
                return

            # Wait with timeout (30 seconds)
            granted, wait_time = self.court.queue.wait_for_resource(visitor_id, timeout=30)

            if not granted:
                log(f"Visitor {visitor_id} gave up waiting for {self.name}")
                return

        try:
            # Use the court
            duration = random.randint(self.min_duration, self.max_duration)
            log(f"Visitor {visitor_id} using {self.name} court for {duration} minutes")

            # Simulate the activity
            time.sleep(duration * 0.1)

        finally:
            # Release the court
            self.court.queue.release_resource(visitor_id)
            log_sport_game(self.name, duration)

