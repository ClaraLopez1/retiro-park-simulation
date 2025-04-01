import time
from Activities.activity import Activity
import threading

class VisitCafe(Activity):
    def __init__(self, cafe):
        super().__init__(f"Visiting {cafe.name}", 1, 2)
        self.cafe = cafe

    def perform(self, visitor_id):
        time.sleep(self.duration)
        print(f"Visitor {visitor_id} arrived at {self.cafe.name}")
        done_event = threading.Event()
        self.cafe.enqueue_visitor(visitor_id, done_event)
        print(f"Visitor {visitor_id} is waiting for coffee at {self.cafe.name}")
        done_event.wait()
        print(f"Visitor {visitor_id} got their coffee and is leaving {self.cafe.name}")
