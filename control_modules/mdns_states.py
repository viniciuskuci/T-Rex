from .base_fsm import State
import time

class DiscoverState(State):

    def run(self):
        print("Running Discover State")
        time.sleep(2)
        self.context.set_state(AnnounceState())
        return
    
class AnnounceState(State):

    def run(self):
        print("Running Announce State")
        time.sleep(2)
        self.context.set_state(DiscoverState())
        return