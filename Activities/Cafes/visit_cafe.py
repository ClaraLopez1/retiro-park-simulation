import time
import random
from Activities.activity import Activity
import threading
from Utils.logger import log
from UI.park_map import get_activity_coord
from Utils.database import log_cafe_order


class VisitCafe(Activity):
    def __init__(self, cafe):
        super().__init__(f"Visit {cafe.name}", min_duration=3, max_duration=8)
        self.cafe = cafe

    def perform(self, visitor_id):
        # First try to get a seat
        seated, seat_position = self.cafe.seating_queue.request_resource(visitor_id)

        if not seated:
            # Check queue length
            queue_length = self.cafe.seating_queue.get_queue_length()

            # Visitor might decide not to wait if queue is too long
            if queue_length > 5 and random.random() < 0.3:
                log(f"Visitor {visitor_id} decided not to wait for seat at {self.cafe.name}")
                self.cafe.seating_queue.leave_queue(visitor_id)
                return

            # Wait for a seat with timeout
            est_wait = self.cafe.seating_queue.get_estimated_wait_time(visitor_id)
            log(f"Visitor {visitor_id} waiting for seat at {self.cafe.name}. Position: {seat_position}, Est. wait: {est_wait:.1f}s")
            seated, wait_time = self.cafe.seating_queue.wait_for_resource(visitor_id, timeout=20)

            if not seated:
                log(f"Visitor {visitor_id} gave up waiting for seat at {self.cafe.name}")
                return

        try:
            # Now order (get a barista)
            served, service_position = self.cafe.service_queue.request_resource(visitor_id)

            if not served:
                # Wait for service with timeout
                est_wait = self.cafe.service_queue.get_estimated_wait_time(visitor_id)
                log(f"Visitor {visitor_id} waiting for service at {self.cafe.name}. Position: {service_position}, Est. wait: {est_wait:.1f}s")
                served, wait_time = self.cafe.service_queue.wait_for_resource(visitor_id, timeout=15)

                if not served:
                    log(f"Visitor {visitor_id} gave up waiting for service at {self.cafe.name}")
                    return

            try:
                # Order and prepare drink (simulation)
                item = random.choice(self.cafe.menu_items)
                log_cafe_order(visitor_id, self.cafe.name, item.name, item.price)
                log(f"Visitor {visitor_id} ordered {item.name} at {self.cafe.name}")
                time.sleep(1.5)  # Preparation time

            finally:
                # Release barista
                self.cafe.service_queue.release_resource(visitor_id)

            # Enjoy drink
            log(f"Visitor {visitor_id} enjoying {item.name} at {self.cafe.name}")
            duration = random.randint(self.min_duration, self.max_duration)
            time.sleep(duration * 0.1)  # Drinking time

        finally:
            # Release seat
            self.cafe.seating_queue.release_resource(visitor_id)