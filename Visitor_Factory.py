import random
from Visitor import Visitor
from datetime import datetime, timedelta

class VisitorFactory:
    # Defines behavior profiles for different visitor "personas"
    # Each persona has a different weight (preference) for activity types
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

    def __init__(self, activities):
        # List of all available park activities passed in from main simulator
        self.activities = activities

    def create_visitor(self, visitor_id):
        # Randomly assign one of the predefined personas
        persona_name = random.choice(list(self.PERSONAS.keys()))
        preferences = self.PERSONAS[persona_name]
        # Randomize visitor's entry time between 6:00 and 18:00
        entry_hour = random.randint(6, 18)
        # Calculate exit time based on persona behavior
        entry_dt = datetime.strptime(f"{entry_hour:02}:00", "%H:%M")
        exit_dt = self.get_exit(entry_hour, persona_name)
        # Format times for consistency
        entry_time = entry_dt.strftime("%H:%M")
        exit_time = exit_dt.strftime("%H:%M")

        return Visitor(visitor_id, self.activities, persona_name, preferences, entry_time, exit_time)

    def create_visitors(self, count):
        return [self.create_visitor(i) for i in range(count)]

    def get_exit(self, entry_hour, persona_name):
        entry_dt = datetime.strptime(f"{entry_hour:02}:00", "%H:%M")
        # Assign a stay duration based on persona-specific logic
        if persona_name == "Cultural":
            exit_dt = entry_dt + timedelta(hours=random.randint(1, 6))
        elif persona_name == "Sporty":
            exit_dt = entry_dt + timedelta(hours=random.randint(2, 3))
        elif persona_name == "Relaxed":
            exit_dt = entry_dt + timedelta(hours=random.randint(1, 4))
        elif persona_name == "Explorer":
            exit_dt = entry_dt + timedelta(hours=random.randint(1, 5))
        else:
            exit_dt = entry_dt + timedelta(hours=random.randint(1, 4))

        return exit_dt

