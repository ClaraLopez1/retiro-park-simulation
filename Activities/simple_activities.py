from Activities.activity import Activity as activity
from UI.park_map import get_activity_coord

# Each of these classes defines a simple activity available in the park.
# They inherit from the base Activity class and set a specific name, duration range,
# and coordinates using the map layout (get_activity_coord).

class Walking(activity):
    def __init__(self):
        super().__init__("🚶‍ walking", 5, 15)
        self.coords = get_activity_coord(self.name)

class WatchingPerformance(activity):
    def __init__(self):
        super().__init__("🎭 watching a Street Performance", 3, 7)
        self.coords = get_activity_coord(self.name)

class TakingPhotos(activity):
    def __init__(self):
        super().__init__("📸 taking Photos", 2, 5)
        self.coords = get_activity_coord(self.name)

class Running(activity):
    def __init__(self):
        super().__init__("🏃 running", 5, 15)
        self.coords = get_activity_coord(self.name)


class PalacioCristal(activity):
    def __init__(self):
        super().__init__("️🏛️ visiting Palacio de Cristal", 5, 10)
        self.coords = get_activity_coord(self.name)

class AngelCaido(activity):
    def __init__(self):
        super().__init__("🗿 visiting Angel Caido", 5, 15)
        self.coords = get_activity_coord(self.name)

class PalacioVelazquez(activity):
    def __init__(self):
        super().__init__("🖼 visiting Palacio de Velazquez", 5, 10)
        self.coords = get_activity_coord(self.name)