import sched
import time

class Schedule:
    def __init__(self, method, interval_days):
        self.method = method
        self.interval_days = interval_days
        
    def run(self):
        s = sched.scheduler(time.time, time.sleep)

        def perform_method():
            self.method()
            # s.enter(self.interval_days * 24 * 60, 1, perform_method)

        perform_method()
        s.run()
