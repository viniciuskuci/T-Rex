from .base_fsm import State
import select
import sys
import time

class SearchGateway(State):

    def run(self) -> None:
        print("Searching for gateway (10s)... Press enter to find it!")
        rlist, _, _ = select.select([sys.stdin], [], [], 10)
        if rlist:
            input()
            print("Gateway found! Changing state...")
            self.context.set_state(GatewayFound())
        else:
            print("No gateway found. Changing state...")
            self.context.set_state(GatewayNotFound())

class GatewayNotFound(State):

    def run(self) -> None:
        print("State GatewayNotFound. Do something here. Sleeping for 3 seconds...")
        time.sleep(3)
        print("Changing state...")
        self.context.set_state(GatewayState())


class GatewayFound(State):

    def run(self) -> None:
        print("State GatewayFound. Do something here. Sleeping for 3 seconds...")
        time.sleep(3)
        print("Changing state...")
        self.context.set_state(WorkerState())


class WorkerState(State):

    def run(self) -> None:
        print("State WorkerState. Working...")
        while True:
            time.sleep(1)
            print(".", end="", flush=True)


class GatewayState(State):

    def run(self) -> None:
        print("State GatewayState. Managing...")
        while True:
            time.sleep(1)
            print(".", end="", flush=True)
