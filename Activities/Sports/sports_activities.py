import threading
import time
import random
from Activities.activity import Activity


class SportActivity(Activity):
    def __init__(self, name, players_needed, min_duration=5, max_duration=15):
        self.name = name
        self.players_needed = players_needed
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.players = []
        self.players_lock = threading.Lock()
        self.start_barrier = threading.Barrier(players_needed, action=self.game_start_action)
        self.finish_barrier = threading.Barrier(players_needed, action=self.game_finish_action)
        self.last_players = []

    def game_start_action(self):
        with self.players_lock:
            current_players = self.players.copy()
            self.last_players = current_players
            print(f"Game of {self.name} is starting with {self.players_needed} players: {current_players}!")
            self.players.clear()

    def game_finish_action(self):
        print(f"Game of {self.name} finished with players: {self.last_players}!")

    def perform(self, visitor_id):
        with self.players_lock:
            self.players.append(visitor_id)
        try:
            self.start_barrier.wait()
        except threading.BrokenBarrierError:
            print(f"Game of {self.name} could not start due to an error!")
            return

        game_duration = random.randint(self.min_duration, self.max_duration)
        time.sleep(game_duration)

        try:
            self.finish_barrier.wait()
        except threading.BrokenBarrierError:
            print(f"Game of {self.name} could not finish properly due to an error!")
            return
