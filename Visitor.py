import random
import threading
import time
from UI.park_map import get_activity_coord
from Utils.logger import log


class Visitor(threading.Thread):
    def __init__(self, visitor_id, park_activities):
        super().__init__()
        self.visitor_id = visitor_id
        self.park_activities = park_activities
        self.coords = (10, 10)
        self.running = False
        self.time_manager = None

    def set_time_manager(self, time_manager):
        self.time_manager = time_manager
        self.time_manager.register_listener(self.handle_time_event)

    def handle_time_event(self, event):
        if event == "open":
            self.running = True
        elif event == "close":
            self.running = False

    def smooth_move(self, start_coords, end_coords, steps=20, step_delay=0.05):
        sx, sy = start_coords
        ex, ey = end_coords
        dx = (ex - sx) / steps
        dy = (ey - sy) / steps
        for i in range(steps):
            self.coords = (sx + dx * (i + 1), sy + dy * (i + 1))
            time.sleep(step_delay)

    def run(self):
        while True:
            if not self.running:
                self.smooth_move(self.coords, (10, 10))
                log(f"Visitor {self.visitor_id} is starting: leaving.")
                break

            activity = random.choice(self.park_activities)
            target_coords = get_activity_coord(activity.name)
            if self.coords != target_coords:
                log(f"Visitor {self.visitor_id} moving from {self.coords} to {target_coords} for {activity.name}")
                self.smooth_move(self.coords, target_coords)

            if not self.running:
                log(f"Visitor {self.visitor_id} stopped before starting {activity.name}")
                continue

            log(f"Visitor {self.visitor_id} is starting: {activity.name} at {self.coords}")
            activity.perform(self.visitor_id)

