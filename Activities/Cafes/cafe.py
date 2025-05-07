import threading
from Utils.logger import log
from Utils.resource_queue import ResourceQueue
from Activities.Cafes.Menu.MenuItem import MenuItem

class Cafe:
    def __init__(self, name, num_baristas, menu_items=None):
        self.name = name
        self.menu_items = menu_items or self._default_menu()
        
        # Queue for barista service
        self.service_queue = ResourceQueue(
            resource_type="cafe",
            resource_name=f"{name}_service",
            capacity=num_baristas
        )
        
        # Queue for seating
        self.seating_queue = ResourceQueue(
            resource_type="cafe",
            resource_name=f"{name}_seating",
            capacity=num_baristas * 3  # Assumption: 3 seats per barista
        )

    def _default_menu(self):
        return [
            MenuItem("Café con leche", 2.50, "Café con leche caliente"),
            MenuItem("Medialuna", 1.20, "Clásica medialuna de manteca"),
            MenuItem("Tostado", 3.00, "Tostado de jamón y queso"),
        ]


