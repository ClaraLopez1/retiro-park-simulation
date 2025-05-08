import random
from Visitor import Visitor
from datetime import datetime, timedelta

class VisitorFactory:
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
        self.activities = activities

    def create_visitor(self, visitor_id):
        persona_name = random.choice(list(self.PERSONAS.keys()))
        preferences = self.PERSONAS[persona_name]

        entry_hour = random.randint(6, 18)  # entra entre las 6 y 18
        exit_hour = random.randint(entry_hour + 1, 22)  # sale después de entrar, hasta las 22
        entry_time = f"{entry_hour:02}:00"
        exit_time = f"{exit_hour:02}:00"

        return Visitor(visitor_id, self.activities, persona_name, preferences, entry_time, exit_time)

    def create_visitors(self, count):
        return [self.create_visitor(i) for i in range(count)]


