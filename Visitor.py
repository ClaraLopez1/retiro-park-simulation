import random
import sqlite3
import threading
import time
from UI.park_map import get_activity_coord
from Utils.database import log_entry, log_exit, log_activity
from Utils.logger import log


class Visitor(threading.Thread):
    def __init__(self, visitor_id, park_activities):
        super().__init__()
        self.visitor_id = visitor_id
        self.park_activities = park_activities
        self.coords = (10, 10)
        self.entered = False
        self.running = False
        self.time_manager = None

    def set_time_manager(self, time_manager):
        self.time_manager = time_manager
        self.time_manager.register_listener(self.handle_time_event)

    def handle_time_event(self, event):
        if event == "open":
            self.running = True
            self.entered = True
            current_time = self.time_manager.get_current_time()
            log_entry(self.visitor_id, current_time)
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

    def choose_activity(self):
        """
        Choose an activity based on time of day.
        Early Morning (6-9): Prefer walking, running
        Midday (9-13): Prefer cultural visits, taking photos
        Afternoon (13-17): Prefer cafes, cultural visits
        Evening (17-22): Prefer sports, boat/bike rentals
        """
        time_of_day = self.time_manager.get_time_of_day()
        current_time = self.time_manager.get_current_time()

        # Group activities by type
        walking_activities = [act for act in self.park_activities if
                              act.name in ["Walking", "Running", "Taking Photos"]]
        cafe_activities = [act for act in self.park_activities if "Visit" in act.name]
        cultural_activities = [act for act in self.park_activities if
                               "Palacio" in act.name or "Angel" in act.name or "Performance" in act.name]
        sport_activities = [act for act in self.park_activities if
                            "Tennis" in act.name or "Football" in act.name or "Padel" in act.name]
        rental_activities = [act for act in self.park_activities if "Renting" in act.name]

        # Set preference weights based on time of day
        if time_of_day == "early_morning":
            weights = {
                "walking": 0.4,  # Highest preference for walking/running in early morning
                "cafe": 0.1,  # Low preference for cafes in early morning
                "cultural": 0.3,  # Low preference for cultural activities
                "sport": 0.1,  # Low preference for sports in early morning
                "rental": 0.1  # Low preference for rentals in early morning
            }
        elif time_of_day == "midday":
            weights = {
                "walking": 0.2,  # Medium preference for walking at midday
                "cafe": 0.3,  # Medium-low preference for cafes at midday
                "cultural": 0.2,  # High preference for cultural visits at midday
                "sport": 0.05,  # Very low preference for sports at midday (too hot)
                "rental": 0.25  # Very low preference for rentals at midday (too hot)
            }
        elif time_of_day == "afternoon":
            weights = {
                "walking": 0.1,  # Very low preference for walking in the afternoon (too hot)
                "cafe": 0.2,  # High preference for cafes in the afternoon
                "cultural": 0.25,  # High preference for cultural visits
                "sport": 0.25,  # Medium-low preference for sports in the afternoon
                "rental": 0.2  # Low preference for rentals in the afternoon
            }
        elif time_of_day == "evening":
            weights = {
                "walking": 0.4,  # Medium preference for walking in the evening (cooler)
                "cafe": 0.1,  # Low preference for cafes in the evening
                "cultural": 0.39,  # Low preference for cultural activities in the evening
                "sport": 0.01,  # High preference for sports in the evening
                "rental": 0.1  # High preference for boating/biking in the evening
            }
        else:  # night or unexpected value - use equal weights
            weights = {
                "walking": 0.4,
                "cafe": 0.2,
                "cultural": 0.2,
                "sport": 0.0,
                "rental": 0.2
            }

        # Create a weighted list of all activities
        all_activities = []
        all_activities.extend([(act, weights["walking"]) for act in walking_activities])
        all_activities.extend([(act, weights["cafe"]) for act in cafe_activities])
        all_activities.extend([(act, weights["cultural"]) for act in cultural_activities])
        all_activities.extend([(act, weights["sport"]) for act in sport_activities])
        all_activities.extend([(act, weights["rental"]) for act in rental_activities])

        # Handle any activities that didn't fit into our categories
        uncategorized = [act for act in self.park_activities if act not in
                         [a for a_list in [walking_activities, cafe_activities, cultural_activities,
                                           sport_activities, rental_activities] for a in a_list]]
        all_activities.extend([(act, 0.2) for act in uncategorized])  # Give uncategorized activities a medium weight

        # Select an activity based on weights
        activities, weights = zip(*all_activities) if all_activities else (self.park_activities, None)

        # If we have weights, use them for selection
        if weights and any(w > 0 for w in weights):
            selected_activity = random.choices(activities, weights=weights, k=1)[0]
        else:
            # Fallback to random choice if we have no valid weights
            selected_activity = random.choice(self.park_activities)

        # Log the selection with time information
        log(f"Visitor {self.visitor_id} at time {current_time} ({time_of_day}) selected activity: {selected_activity.name}")
        log_activity(self.visitor_id, selected_activity.name, current_time)
        return selected_activity


    def run(self):
        while not self.entered:
            time.sleep(0.01)

        while True:
            if not self.running:
                self.smooth_move(self.coords, (10, 10))
                current_time = self.time_manager.get_current_time()
                log_exit(self.visitor_id, current_time)
                log(f"Visitor {self.visitor_id} is starting: leaving.")
                break

            activity = self.choose_activity()
            target_coords = get_activity_coord(activity.name)
            if self.coords != target_coords:
                log(f"Visitor {self.visitor_id} moving from {self.coords} to {target_coords} for {activity.name}")
                self.smooth_move(self.coords, target_coords)

            if not self.running:
                continue

            log(f"Visitor {self.visitor_id} is starting: {activity.name} at {self.coords}")
            activity.perform(self.visitor_id)


