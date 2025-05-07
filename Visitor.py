import random
import threading
import time
from UI.park_map import get_activity_coord
from Utils.logger import log


class Visitor(threading.Thread):
    # Define personas, values above 1.0 indicate interest and values below 1.0 indicate decreased interest.
    PERSONAS = {
       "Cultural": {
           "cultural": 2.0, 
           "walking": 1.2,
           "cafe": 1.5,   
           "sport": 0.3,
           "rental": 0.7
       },
       "Sporty": {
           "cultural": 0.5,
           "walking": 1.0,
           "cafe": 0.7,
           "sport": 2.0,
           "rental": 1.5
       },
       "Relaxed": {
           "cultural": 1.2,
           "walking": 1.5,
           "cafe": 1.8,
           "sport": 0.2,
           "rental": 1.0
       },
       "Explorer": {
           "cultural": 1.3,
           "walking": 1.7,
           "cafe": 0.8,
           "sport": 0.6,
           "rental": 1.8
       }
   }

    def __init__(self, visitor_id, park_activities):
        super().__init__()
        self.visitor_id = visitor_id
        self.park_activities = park_activities
        self.coords = (10, 10)
        self.running = False
        self.time_manager = None
        
        # Assign a random persona
        self.persona_name = random.choice(list(self.PERSONAS.keys()))
        self.persona_preferences = self.PERSONAS[self.persona_name]
        log(f"Visitor {self.visitor_id} has persona: {self.persona_name}")

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
            selected_activity = random.choice(self.park_activities)
        
        # Log including persona information
        log(f"Visitor {self.visitor_id} ({self.persona_name}) at time {current_time} ({time_of_day}) selected activity: {selected_activity.name}")
        
        return selected_activity

    def run(self):
        while True:
            if not self.running:
                self.smooth_move(self.coords, (10, 10))
                log(f"Visitor {self.visitor_id} is starting: leaving.")
                break

            activity = self.choose_activity()
            target_coords = get_activity_coord(activity.name)
            if self.coords != target_coords:
                log(f"Visitor {self.visitor_id} moving from {self.coords} to {target_coords} for {activity.name}")
                self.smooth_move(self.coords, target_coords)

            if not self.running:
                log(f"Visitor {self.visitor_id} stopped before starting {activity.name}")
                continue

            log(f"Visitor {self.visitor_id} is starting: {activity.name} at {self.coords}")
            activity.perform(self.visitor_id)


