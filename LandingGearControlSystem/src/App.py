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

class GearFault(Enum):
    SENSOR_MISMATCH = auto()
    TIMEOUT_ERROR = auto()
    HYDRAULIC_FAILURE = auto()
    NONE = auto()

class GearSensor:
    def __init__(self, name):
        self.name= name
        self.position = GearPosition.UP
    
    def get_position(self):
        return self.position
    
    def set_position(self, position):
        self.position = position

class TripleRedundancy:
    def __init__(self, sensors):
        if len(sensors) == 3:
            self.sensors = sensors
        else:
            return
    
    def get_position(self):
        sensor_position_one = self.sensors[0].get_position()
        sensor_position_two = self.sensors[1].get_position()
        sensor_position_three = self.sensors[2].get_position()

        if sensor_position_one == sensor_position_two or sensor_position_one == sensor_position_three:
            return sensor_position_one
        if sensor_position_two == sensor_position_three:
            return sensor_position_two
        else:
            return GearPosition.UNKNOWN

    def set_position(self, position):
        for sensor in self.sensors:
            sensor.set_position(position)


class LandingGearController:
    def __init__(self):
        self.state = GearState.UP_LOCKED
        self.fault = GearFault.NONE

        sensor_1 = GearSensor("Sensor1")
        sensor_2 = GearSensor("Sensor2")
        sensor_3 = GearSensor("Sensor3")

        self.sensor = TripleRedundancy([sensor_1, sensor_2, sensor_3])


    def log(self, message):
        print(f"[{self.state.name}] {message}")

    def command_gear_down(self):

        position = self.sensor.get_position()

        if position == GearPosition.UNKNOWN:
            self.fault = GearFault.SENSOR_MISMATCH
            self.log(f"Fault detected: {self.fault}.")
            return

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
            self.log("Invalid command rejected.")
            

    def command_gear_up(self):

        position = self.sensor.get_position()

        if position == GearPosition.UNKNOWN:
            self.fault = GearFault.SENSOR_MISMATCH
            self.log(f"Fault detected: {self.fault}.")
            return

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
            self.log("Invalid command rejected.")

    def reset_system(self):
        self.state = GearState.UP_LOCKED
        self.sensor.set_position(GearPosition.UP)
        self.fault = GearFault.NONE


controller = LandingGearController()
controller.command_gear_down()
controller.command_gear_up()
