from enum import Enum, auto
import time

class GearState(Enum):
    UP_LOCKED = auto()
    TRANSITIONING_DOWN = auto()
    DOWN_LOCKED = auto()
    TRANSITIONING_UP = auto()
    ERROR = auto()

class GearPosition(Enum):
    UP = auto()
    DOWN = auto()
    UNKNOWN = auto()

class GearSensor:
    def __init__(self):
        self.position = GearPosition.UP
    
    def get_position(self):
        return self.position
    
    def set_position(self, position):
        self.position = position

class LandingGearController:
    def __init__(self):
        self.state = GearState.UP_LOCKED
        self.sensor = GearSensor()

    def log(self, message):
        print(f"[{self.state.name}] {message}")

    def command_gear_down(self):

        position = self.sensor.get_position()
    
        if self.state == GearState.DOWN_LOCKED and position == GearPosition.DOWN:
            self.log("Command rejected: gear already down.")
            return
        
        if self.state == GearState.UP_LOCKED and position == GearPosition.UP:
            self.state = GearState.TRANSITIONING_DOWN
            self.sensor.set_position(GearPosition.UNKNOWN)
            self.log("Gear deploying.")
            time.sleep(1)
            self.state = GearState.DOWN_LOCKED
            self.sensor.set_position(GearPosition.DOWN)
            self.log("Gear locked down.")
        else:
            self.state = GearState.ERROR 
            self.sensor.set_position(GearPosition.UNKNOWN)
            self.log("ERROR")

    def command_gear_up(self):

        position = self.sensor.get_position()

        if self.state == GearState.UP_LOCKED and position == GearPosition.UP:
            self.log("Command rejected: gear already up.")
            return

        if self.state == GearState.DOWN_LOCKED and position == GearPosition.DOWN:
            self.state = GearState.TRANSITIONING_UP
            self.sensor.set_position(GearPosition.UNKNOWN)
            self.log("Gear retracting.")
            time.sleep(1)
            self.state = GearState.UP_LOCKED
            self.sensor.set_position(GearPosition.UP)
            self.log("Gear locked up.")
        else:
            self.state = GearState.ERROR 
            self.sensor.set_position(GearPosition.UNKNOWN)
            self.log("ERROR")

controller = LandingGearController()
controller.command_gear_down()
controller.command_gear_up()
