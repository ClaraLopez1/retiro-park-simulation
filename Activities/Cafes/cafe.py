import threading
import time
import random
from queue import Queue
from Utils.logger import log


class Barista(threading.Thread):
    def __init__(self, barista_id, cafe):
        super().__init__()
        self.barista_id = barista_id
        self.cafe = cafe

    def run(self):
        while True:
            visitor_id, done_event = self.cafe.queue.get()
            prep_time = random.randint(3, 7)
            log(f"[{self.cafe.name}] Barista {self.barista_id} is preparing coffee for Visitor {visitor_id} ({prep_time} seconds)")
            time.sleep(prep_time)
            log(f"[{self.cafe.name}] Barista {self.barista_id} finished serving Visitor {visitor_id}")
            done_event.set()
            self.cafe.queue.task_done()


class Cafe:
    def __init__(self, name, num_baristas):
        self.name = name
        self.queue = Queue()
        self.baristas = [Barista(i, self) for i in range(num_baristas)]
        for barista in self.baristas:
            barista.start()

    def enqueue_visitor(self, visitor_id, done_event):
        self.queue.put((visitor_id, done_event))


#TODO:consider adding menu items with price