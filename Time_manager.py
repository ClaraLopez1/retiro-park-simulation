import threading
import time
from datetime import datetime, timedelta
import random
from Utils.logger import log

class TimeManager(threading.Thread):
    # Weekday names to simulate the day of the week in the GUI
    WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def __init__(self, time_scale=0.2):
        super().__init__()
        self.time_scale = time_scale # Speed of the simulation: 1 real second = 5 simulated minutes
        self._lock = threading.Lock() # Lock to synchronize access to the time
        self.current_time = datetime.strptime("06:00", "%H:%M")  # Simulation starts at 6:00 AM
        self.current_day = random.choice(self.WEEKDAYS) # Randomly select a weekday
        self.running = True
        self.listeners = [] # List of callbacks (e.g., visitors, GUI) to notify about time events
        self.park_open = False

    def run(self):
        # Start of simulation: mark park as open and notify listeners
        self.park_open = True
        self._notify("open")

        while self.running:
            with self._lock:
                # Advance simulation time by one minute
                self.current_time += timedelta(minutes=1)
                hour = self.current_time.hour
                minute = self.current_time.minute

                # Notify all listeners when the park closes at 22:00
                if hour == 22 and minute == 0:
                    self._notify("close")

            # Wait for the next simulated minute (controlled by time_scale)
            time.sleep(self.time_scale)

        log("Park is closed. Simulation ended.")

    def _notify(self, event):
        # Notify all registered listeners about a specific event (e.g., "open", "close")
        for callback in self.listeners:
            callback(event)

    # Register a new listener (usually visitors or the park controller)
    def register_listener(self, callback):
        self.listeners.append(callback)

    def get_current_time(self):
        with self._lock:
            return self.current_time.strftime("%H:%M")

    def get_current_day(self):
        return self.current_day

    def get_time_of_day(self):
        # Categorize current time into one of the day periods
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
