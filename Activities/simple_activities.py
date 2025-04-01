from Activities.activity import Activity as activity


class Walking(activity):
    def __init__(self):
        super().__init__("Walking", 5, 15)


class WatchingPerformance(activity):
    def __init__(self):
        super().__init__("Watching a Street Performance", 3, 7)


class TakingPhotos(activity):
    def __init__(self):
        super().__init__("Taking Photos", 2, 5)

class Running(activity):
    def __init__(self):
        super().__init__("Running", 5, 15)


#TODO: visit monument