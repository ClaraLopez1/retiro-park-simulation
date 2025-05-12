import threading
import time
import random
from datetime import datetime

from Activities.activity import Activity
from Utils.logger import log
from UI.park_map import get_activity_coord
from queue import Queue
from Utils.database import log_sport_game, log_sport_wait_time


class SportCourt:
    """Represents a shared resource (court) that must be acquired before starting a game."""
    def __init__(self, sport_type):
        self.sport_type = sport_type
        self.lock = threading.Lock() # Ensures only one game can use the court at a time.


class SportActivity(Activity):
    """
      Represents a coordinated sport activity where a minimum number of players
      must be present and a court must be free before the game can start.
      """
    def __init__(self, name, players_needed, court, min_duration=5, max_duration=15):
        self.name = name
        self.players_needed = players_needed
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.players = []
        self.players_lock = threading.Lock()
        self.condition = threading.Condition() # Used to wait for enough players or notify start
        self.game_in_progress = False
        self.last_players = []
        self.coords = get_activity_coord(self.name)
        self.court = court  # Shared court resource
        self.waiting_queue = Queue() # FIFO queue of (visitor_id, arrival_time)

    def perform(self, visitor_id):
        arrival_time = datetime.now()
        self.waiting_queue.put((visitor_id, arrival_time))
        log(f"⏳Visitor {visitor_id} joined the waiting queue for {self.name}.")

        with self.condition:
            wait_times = []

            # If a game is already in progress, wait until notified
            while self.game_in_progress:
                self.condition.wait()

            # Check if we have enough players to start a game
            if self.waiting_queue.qsize() >= self.players_needed:
                self.game_in_progress = True
                self.last_players = []
                start_time = datetime.now()

                # Collect enough players from the queue and calculate their wait times
                for _ in range(self.players_needed):
                    vid, arr_time = self.waiting_queue.get()
                    wait = max(0, int((start_time - arr_time).total_seconds()))
                    wait_times.append((vid, arr_time, wait))
                    self.last_players.append(vid)  # solo el ID
                log(f"\n---🎾Game of {self.name} START ---")
                log(f"Players: {self.last_players}")
                self.condition.notify_all() # Wake any waiting threads
            else:
                self.condition.wait() # Not enough players yet; wait

        # Try to acquire the court
        acquired = self.court.lock.acquire(blocking=False)
        if acquired:
            game_duration = random.randint(self.min_duration, self.max_duration)
            log(f"Game of {self.name} will last {game_duration} seconds.")
            time.sleep(game_duration) # Simulate game
            with self.condition:
                log(f"\n---🏁 Game of {self.name} FINISHED ---")
                log(f"Players: {self.last_players}")
                self.game_in_progress = False
                self.condition.notify_all() # Notify threads that game is over

            self.court.lock.release()
            log_sport_game(self.name, game_duration, self.last_players)
            for vid, arr_time, wait in wait_times:
                log_sport_wait_time(vid, self.name, arr_time, start_time, wait)

            log(f"Court lock released for {self.name}.")
        else:
            # If court is occupied, wait until it's free
            with self.condition:
                while self.game_in_progress:
                    self.condition.wait()
