import random
from Activities.activity import Activity
import threading
from Utils.logger import log
from UI.park_map import get_activity_coord
from Utils.database import log_cafe_order


class VisitCafe(Activity):
    def __init__(self, cafe):
        super().__init__(f"Visiting {cafe.name}", 1, 2)
        self.cafe = cafe
        self.coords = get_activity_coord(self.name)

    def perform(self, visitor_id):
        item = random.choice(self.cafe.menu)
        log(f"Visitor {visitor_id} is moving to {self.coords} to visit {self.cafe.name}.")
        log(f"Visitor {visitor_id} arrived at {self.cafe.name} and orders '{item.name}' (${item.price:.2f}): {item.description}")

        done_event = threading.Event()
        self.cafe.enqueue_visitor(visitor_id, done_event)

        log(f"Visitor {visitor_id} is waiting for '{item.name}' at {self.cafe.name}")
        done_event.wait()
        log(f"Visitor {visitor_id} got their '{item.name}' and is leaving {self.cafe.name}\n")
        log_cafe_order(visitor_id, self.cafe.name, item.name, item.price)
