from Activities.activity_factory import ActivityFactory
from UI.gui import start_gui
from Visitor_Factory import VisitorFactory
from Activities.Renting.rent_bike import RentBike
from Activities.Renting.rent_boat import RentBoat
from Activities.Sports.sports_activities import SportActivity

from Time_manager import TimeManager
from Utils.logger import log, set_time_manager
from Visitor import Visitor
from Utils.database import init_db


class RetiroPark:
    def __init__(self, num_visitors):
        init_db()
        self.activities = ActivityFactory().create_all()
        self.time_manager = TimeManager(
            time_scale=0.2,
        )
        self.time_manager.register_listener(self.handle_time_event)

        self.visitors = VisitorFactory(self.activities).create_visitors(num_visitors)
        set_time_manager(self.time_manager)

        for visitor in self.visitors:
            visitor.set_time_manager(self.time_manager)

    def handle_time_event(self, event):
        if event == "close":
            for activity in self.activities:
                if isinstance(activity, SportActivity):
                    with activity.condition:
                        activity.condition.notify_all()
                elif isinstance(activity, RentBike):
                    activity.bike_rental.notify_closure()
                elif isinstance(activity, RentBoat):
                    activity.boat_rental.notify_closure()

    def start(self):
        self.time_manager.start()
        for visitor in self.visitors:
            visitor.start()
        start_gui(self.visitors, self.time_manager)



if __name__ == "__main__":
    park = RetiroPark(num_visitors=200)
    park.start()
