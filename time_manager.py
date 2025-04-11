from datetime import datetime, time, timedelta
import threading
import time as time_module

class TimeManager:
    WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    def __init__(self, start_time=None, time_scale=0.2, start_day="Monday"):
        """
        Initialize the TimeManager.
        
        Args:
            start_time (datetime, optional): The starting time. Defaults to current time.
            time_scale (int): Number of real seconds per simulation minute. Defaults to 0.2.
            start_day (str): The day to start the simulation on. Defaults to "Monday".
        """
        self.time_scale = time_scale
        self.start_time = start_time if start_time else datetime.now()
        self.current_time = self.start_time
        self.current_day = start_day
        self.last_update = datetime.now()
        self.is_running = False
        self._lock = threading.Lock()
        self.day_changed = False  # Flag to track day changes
        
    def start(self):
        """Start the time manager."""
        if not self.is_running:
            self.is_running = True
            self._time_thread = threading.Thread(target=self._update_time)
            self._time_thread.daemon = True
            self._time_thread.start()
            print("Time manager started")  # Debug print
        
    def stop(self):
        """Stop the time manager."""
        self.is_running = False
        if hasattr(self, '_time_thread'):
            self._time_thread.join()
            print("Time manager stopped")  # Debug print
            
    def _update_time(self):
        """Update the current simulation time based on elapsed real time."""
        print("Time update thread started")  # Debug print
        while self.is_running:
            try:
                now = datetime.now()
                elapsed_real_seconds = (now - self.last_update).total_seconds()
                elapsed_simulation_minutes = elapsed_real_seconds / self.time_scale
                
                # Update the current time
                with self._lock:
                    previous_day = self.current_day
                    self.current_time += timedelta(minutes=elapsed_simulation_minutes)
                    
                    # Check if we've crossed midnight
                    if self.current_time.hour == 0 and self.current_time.minute == 0:
                        # Move to next day
                        current_day_index = self.WEEKDAYS.index(self.current_day)
                        next_day_index = (current_day_index + 1) % 7
                        self.current_day = self.WEEKDAYS[next_day_index]
                        self.day_changed = True
                        print(f"Day changed from {previous_day} to {self.current_day}")
                    
                    # Skip night hours (10:10 PM to 5:55 AM)
                    if (self.current_time.hour == 22 and self.current_time.minute >= 10) or (self.current_time.hour < 6 and self.current_time.minute < 55):
                        # Jump to 5:55 AM the next day
                        self.current_time = self.current_time.replace(hour=5, minute=55, second=0, microsecond=0)
                        
                        # Always move to next day when skipping night hours
                        current_day_index = self.WEEKDAYS.index(self.current_day)
                        next_day_index = (current_day_index + 1) % 7
                        self.current_day = self.WEEKDAYS[next_day_index]
                        self.day_changed = True
                        print(f"Skipping night hours. Now it's {self.current_day} at {self.current_time.strftime('%I:%M %p')}")
                
                self.last_update = now
                time_module.sleep(0.1)  # Small sleep to prevent CPU overuse
                
            except Exception as e:
                print(f"Error in time update thread: {e}")
                time_module.sleep(1)  # Sleep longer on error
        
    def get_current_time(self):
        """Get the current simulation time."""
        with self._lock:
            return self.current_time
            
    def get_current_day(self):
        """Get the current day of the week."""
        with self._lock:
            return self.current_day
            
    def is_weekend(self):
        """Check if the current day is a weekend."""
        return self.current_day in ['Saturday', 'Sunday']
        
    def is_park_open(self):
        """Check if the park is currently open."""
        current = self.get_current_time()
        park_open_time = time(6, 0)  # 6:00 AM
        park_close_time = time(22, 0)  # 10:00 PM
        
        current_time = current.time()
        return park_open_time <= current_time <= park_close_time
        
    def is_park_closing_soon(self, minutes=30):
        """Check if the park is closing soon (within the specified minutes)."""
        current = self.get_current_time()
        park_close_time = time(22, 0)  # 10:00 PM
        
        current_time = current.time()
        time_until_close = datetime.combine(datetime.today(), park_close_time) - datetime.combine(datetime.today(), current_time)
        
        return 0 < time_until_close.total_seconds() / 60 <= minutes
        
    def get_time_of_day(self):
        """Get the time of day (morning, afternoon, evening, night)."""
        with self._lock:
            hour = self.current_time.hour
            if 5 <= hour < 12:
                return "morning"
            elif 12 <= hour < 17:
                return "afternoon"
            elif 17 <= hour < 21:
                return "evening"
            else:
                return "night"
            
    def get_time_scale_description(self):
        """Get a human-readable description of the time scale."""
        return f"1 real second = {1/self.time_scale:.1f} simulation minutes" 