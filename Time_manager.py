import threading
import time
from datetime import datetime, timedelta
import random

class TimeManager(threading.Thread):
    WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def __init__(self, time_scale=0.2):
        super().__init__()
        self.time_scale = time_scale
        self._lock = threading.Lock()
        self.current_time = datetime.strptime("06:00", "%H:%M")
        self.current_day = random.choice(self.WEEKDAYS)
        self.running = True
        self.listeners = []
        self.park_open = False

    def run(self):
        self.park_open = True
        self._notify("open")

        while self.running:
            with self._lock:
                self.current_time += timedelta(minutes=1)
                hour = self.current_time.hour
                minute = self.current_time.minute

                if hour == 20 and minute == 0:
                    self._notify("closing sport activities")

                if hour == 22 and minute == 0:
                    self.park_open = False
                    self._notify("close")
                    self.running = False  # End simulation
                    break

            time.sleep(self.time_scale)

    def _notify(self, event):
        for callback in self.listeners:
            callback(event)

    def register_listener(self, callback):
        self.listeners.append(callback)

    def get_current_time(self):
        with self._lock:
            return self.current_time.strftime("%H:%M")

    def get_current_day(self):
        return self.current_day

    def get_time_of_day(self):
        hour = self.current_time.hour
        if 6 <= hour < 9:
            return "early_morning"
        elif 9 <= hour < 13:
            return "midday"
        elif 13 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 22:
            return "evening"
        else:
            return "night"

    def is_park_open(self):
        return self.park_open
