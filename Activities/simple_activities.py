from Activities.activity import Activity as activity
from UI.park_map import get_activity_coord


class Walking(activity):
    def __init__(self):
        super().__init__("Walking", 5, 15)
        self.coords = get_activity_coord(self.name)

class WatchingPerformance(activity):
    def __init__(self):
        super().__init__("Watching a Street Performance", 3, 7)
        self.coords = get_activity_coord(self.name)

class TakingPhotos(activity):
    def __init__(self):
        super().__init__("Taking Photos", 2, 5)
        self.coords = get_activity_coord(self.name)

class Running(activity):
    def __init__(self):
        super().__init__("Running", 5, 15)
        self.coords = get_activity_coord(self.name)


class PalacioCristal(activity):
    def __init__(self):
        super().__init__("Palacio de Cristal", 5, 10)
        self.coords = get_activity_coord(self.name)

class AngelCaido(activity):
    def __init__(self):
        super().__init__("Angel Caido", 5, 15)
        self.coords = get_activity_coord(self.name)

class PalacioVelazquez(activity):
    def __init__(self):
        super().__init__("Palacio de Velazquez", 5, 10)
        self.coords = get_activity_coord(self.name)