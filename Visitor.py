import random
import threading
import time
from UI.park_map import get_activity_coord
from Utils.database import log_entry, log_exit, log_activity
from Utils.logger import log


class Visitor(threading.Thread):
    def __init__(self, visitor_id, park_activities, persona_name, persona_preferences, entry_time, exit_time):
        super().__init__()
        self.visitor_id = visitor_id
        self.park_activities = park_activities
        self.persona_name = persona_name
        self.persona_preferences = persona_preferences
        self.coords = (10, 10)
        self.entered = False
        self.running = False
        self.time_manager = None
        self.entry_time_str = entry_time
        self.exit_time_str = exit_time

    def set_time_manager(self, time_manager):
        self.time_manager = time_manager
        self.time_manager.register_listener(self.handle_time_event)

    def handle_time_event(self, event):
        if event == "open":
            pass
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
        Choose an activity based on time of day and persona preferences.
        """
        TIME_INFLUENCE = 0.75    # 75% influence
        PERSONA_INFLUENCE = 0.25 # 25% influence

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

        # Set base weights based on time of day
        if time_of_day == "early_morning":
            time_weights = {
                "walking": 0.4,
                "cafe": 0.1,
                "cultural": 0.3,
                "sport": 0.1,
                "rental": 0.1
            }
        elif time_of_day == "midday":
            time_weights = {
                "walking": 0.2,
                "cafe": 0.3,
                "cultural": 0.2,
                "sport": 0.05,
                "rental": 0.25
            }
        elif time_of_day == "afternoon":
            time_weights = {
                "walking": 0.1,
                "cafe": 0.2,
                "cultural": 0.25,
                "sport": 0.25,
                "rental": 0.2
            }
        elif time_of_day == "evening":
            time_weights = {
                "walking": 0.4,
                "cafe": 0.1,
                "cultural": 0.39,
                "sport": 0.01,
                "rental": 0.1
            }
        else:  # night or unexpected value
            time_weights = {
                "walking": 0.4,
                "cafe": 0.2,
                "cultural": 0.2,
                "sport": 0.0,
                "rental": 0.2
            }

        # Calculate combined weights using weighted average and normalize
        combined_weights = {}
        for category in time_weights:
            # Get persona preference (default to 1.0 if not specified)
            persona_preference = self.persona_preferences.get(category, 1.0)

            # Calculate weighted average, normalizing persona preferences
            combined_weights[category] = (time_weights[category] * TIME_INFLUENCE) + \
                                        (persona_preference * PERSONA_INFLUENCE / 2.0)

        # Normalize weights to sum to 1.0
        weight_sum = sum(combined_weights.values())
        if weight_sum > 0:  # Avoid division by zero
            for category in combined_weights:
                combined_weights[category] /= weight_sum

        # Create weighted list of activities using combined weights
        all_activities = []
        all_activities.extend([(act, combined_weights["walking"]) for act in walking_activities])
        all_activities.extend([(act, combined_weights["cafe"]) for act in cafe_activities])
        all_activities.extend([(act, combined_weights["cultural"]) for act in cultural_activities])
        all_activities.extend([(act, combined_weights["sport"]) for act in sport_activities])
        all_activities.extend([(act, combined_weights["rental"]) for act in rental_activities])

        # Handle uncategorized activities
        uncategorized = [act for act in self.park_activities if act not in
                        [a for a_list in [walking_activities, cafe_activities, cultural_activities,
                                          sport_activities, rental_activities] for a in a_list]]
        all_activities.extend([(act, 0.2) for act in uncategorized])

        # Select an activity based on weights
        activities, weights = zip(*all_activities) if all_activities else (self.park_activities, None)

        if weights and any(w > 0 for w in weights):
            selected_activity = random.choices(activities, weights=weights, k=1)[0]
        else:
            # Fallback to random choice if we have no valid weights
            selected_activity = random.choice(self.park_activities)

        log_activity(self.visitor_id, selected_activity.name, current_time)
        return selected_activity

    def run(self):
        # Wait until TimeManager is initialized and park is officially open
        while not self.time_manager or not self.time_manager.is_park_open():
            time.sleep(0.05)

        # Wait until the visitor's assigned entry time
        while self.time_manager.get_current_time() < self.entry_time_str:
            time.sleep(0.1)

        # Mark visitor as active and log their entry
        self.running = True
        self.entered = True
        log_entry(self.visitor_id, self.entry_time_str, self.persona_name)

        # Main loop: keeps the visitor inside the park until exit time or park closes
        while True:
            # Check if it's time to leave the park
            if not self.running or self.time_manager.get_current_time() >= self.exit_time_str:
                self.running = False
                self.smooth_move(self.coords, (10, 10))
                log_exit(self.visitor_id, self.time_manager.get_current_time())
                log(f"Visitor {self.visitor_id} is leaving.")
                break

            # Select next activity based on time of day and persona
            activity = self.choose_activity()
            target_coords = get_activity_coord(activity.name)
            # Move to the activity location with smooth animation
            if self.coords != target_coords:
                self.smooth_move(self.coords, target_coords)
            # Check again in case running status changed during movement
            if not self.running:
                continue

            log(f"Visitor {self.visitor_id} is starting: {activity.name}")
            activity.perform(self.visitor_id)


