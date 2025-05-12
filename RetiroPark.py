from Activities.activity_factory import ActivityFactory
from UI.gui import start_gui
from Visitor_Factory import VisitorFactory
from Activities.Renting.rent_bike import RentBike
from Activities.Renting.rent_boat import RentBoat
from Activities.Sports.sports_activities import SportActivity
from Time_manager import TimeManager
from Utils.logger import log, set_time_manager
from Utils.database import init_db


class RetiroPark:
    def __init__(self, num_visitors):
        # Initialize the SQLite database and its tables
        init_db()

        # Create all possible park activities (sports, cafes, rentals, etc.)
        self.activities = ActivityFactory().create_all()

        # Create the global time manager, which simulates a full day
        self.time_manager = TimeManager(
            time_scale=0.2,
        )

        # Register RetiroPark as a listener to receive time events (e.g. "close")
        self.time_manager.register_listener(self.handle_time_event)

        # Create all visitors using predefined personas and entry/exit times
        self.visitors = VisitorFactory(self.activities).create_visitors(num_visitors)

        # Provide the global time manager to the logger for timestamped logs
        set_time_manager(self.time_manager)

        # Each visitor gets a reference to the TimeManager to synchronize their behavior
        for visitor in self.visitors:
            visitor.set_time_manager(self.time_manager)

    def handle_time_event(self, event):
        # When park closes, notify all activities to stop accepting participants
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
        log("Retiro Park is opening!")

        # Start the clock thread
        self.time_manager.start()

        # Start a thread for each visitor
        for visitor in self.visitors:
            visitor.start()

        # Launch the real-time GUI (Tkinter loop)
        start_gui(self.visitors, self.time_manager)



if __name__ == "__main__":
    park = RetiroPark(num_visitors=500)
    park.start()
