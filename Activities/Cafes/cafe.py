import threading
import time
import random
from queue import Queue

from Activities.Cafes.Menu.MenuItem import MenuItem
from Utils.logger import log


class Barista(threading.Thread):
    def __init__(self, barista_id, cafe):
        super().__init__()
        self.barista_id = barista_id
        self.cafe = cafe

    def run(self):
        while True:
            visitor_id, done_event = self.cafe.queue.get()
            prep_time = random.randint(1, 3)
            time.sleep(prep_time)
            log(f"[{self.cafe.name}] Barista {self.barista_id} finished serving Visitor {visitor_id}")
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

    def enqueue_visitor(self, visitor_id, done_event):
        self.queue.put((visitor_id, done_event))


