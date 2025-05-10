import threading
import time
import random
from datetime import datetime
from queue import Queue

from Activities.Cafes.Menu.MenuItem import MenuItem
from Utils.database import log_cafe_wait_time
from Utils.logger import log


class Barista(threading.Thread):
    def __init__(self, barista_id, cafe):
        super().__init__()
        self.barista_id = barista_id
        self.cafe = cafe

    def run(self):
        while True:
            visitor_id, done_event, arrival_time = self.cafe.queue.get()
            served_time = datetime.now()
            wait_duration = int((served_time - arrival_time).total_seconds())

            prep_duration = random.randint(1, 3)
            time.sleep(prep_duration)

            log(f"[{self.cafe.name}] Barista {self.barista_id} finished serving Visitor {visitor_id}")
            log_cafe_wait_time(visitor_id, self.cafe.name, arrival_time, served_time, prep_duration,
                               wait_duration)

            done_event.set()
            self.cafe.queue.task_done()


class Cafe:
    def __init__(self, name, num_baristas, menu_items=None):
        self.name = name
        self.queue = Queue()
        self.baristas = [Barista(i, self) for i in range(num_baristas)]
        for barista in self.baristas:
            barista.start()
        self.menu = menu_items or self._default_menu()

    def _default_menu(self):
        return [
            MenuItem("Café con leche", 2.50, "Café con leche caliente"),
            MenuItem("Medialuna", 1.20, "Clásica medialuna de manteca"),
            MenuItem("Tostado", 3.00, "Tostado de jamón y queso"),
        ]

    def enqueue_visitor(self, visitor_id, done_event, arrival_time):
        self.queue.put((visitor_id, done_event, arrival_time))


