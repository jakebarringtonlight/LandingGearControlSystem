from enum import Enum, auto
import time

class GearState(Enum):
    UP_LOCKED = auto()
    TRANSITIONING_DOWN = auto()
    DOWN_LOCKED = auto()
    TRANSITIONING_UP = auto()
    ERROR = auto()

class LandingGearController:
    def __init__(self):
        self.state = GearState.UP_LOCKED

    def log(self, message):
        print(f"[{self.state.name}] {message}")

    def command_gear_down(self):
        if self.state == GearState.UP_LOCKED:
            self.state = GearState.TRANSITIONING_DOWN
            self.log("Gear deploying")
            time.sleep(1)
            self.state = GearState.DOWN_LOCKED
            self.log("Gear locked down")
        else:
            self.log("Command rejected")

    def command_gear_up(self):
        if self.state == GearState.DOWN_LOCKED:
            self.state = GearState.TRANSITIONING_UP
            self.log("Gear retracting")
            time.sleep(1)
            self.state = GearState.UP_LOCKED
            self.log("Gear locked up")
        else:
            self.log("Command rejected")



controller = LandingGearController()
controller.command_gear_down()
controller.command_gear_up()