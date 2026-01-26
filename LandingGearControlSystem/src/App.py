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

class GearCommand(Enum):
    GEAR_UP = auto()
    GEAR_DOWN = auto()
    RESET = auto()
    INFO = auto()
    SHUTDOWN = auto()

class GearSensor:
    def __init__(self, name):
        self.name= name
        self.position = GearPosition.DOWN
    
    def get_position(self):
        return self.position
    
    def set_position(self, position):
        self.position = position

class TripleRedundancy:
    def __init__(self, sensors):
        if len(sensors) != 3:
            raise ValueError("3 sensors required.")
        self.sensors = sensors
    
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
        self.system_active = True
        self.state = GearState.DOWN_LOCKED
        self.fault = GearFault.NONE

        sensor_1 = GearSensor("Sensor1")
        sensor_2 = GearSensor("Sensor2")
        sensor_3 = GearSensor("Sensor3")

        self.sensor = TripleRedundancy([sensor_1, sensor_2, sensor_3])

    def log(self, message):
        print(f"{message}")

    def receive_command(self, command: GearCommand):
        if self.system_active != True:
            return

        if self.fault != GearFault.NONE and command != GearCommand.RESET:
            self.log("Command rejected. System experiencing fault. Reset Required.")
            return

        if self.state == GearState.ERROR and command != GearCommand.RESET:
            self.log("Command rejected. System in ERROR. Reset Required.")
            return
        
        if command == GearCommand.GEAR_DOWN:
            self.command_gear_down()
        elif command == GearCommand.GEAR_UP:
            self.command_gear_up()
        elif command ==  GearCommand.RESET:
            self.command_reset_system()
        elif command == GearCommand.INFO:
            self.command_info()
        elif command == GearCommand.SHUTDOWN:
            self.command_shutdown()
        
    def command_gear_down(self):
        position = self.sensor.get_position()

        if position == GearPosition.UNKNOWN:
            self.fault = GearFault.SENSOR_MISMATCH
            self.log(f"Fault detected: {self.fault.name}.")
            return

        if self.state == GearState.DOWN_LOCKED and position == GearPosition.DOWN:
            self.log(f"Command rejected: ")
            self.log(f"GearState: {self.state.name}.")
            self.log(f"GearPosition: {self.sensor.get_position().name}")
            return
        
        if self.state == GearState.UP_LOCKED and position == GearPosition.UP:
            self.state = GearState.TRANSITIONING_DOWN
            self.sensor.set_position(GearPosition.UNKNOWN)
            self.log(f"GearState: {self.state.name}.")
            time.sleep(1)
            self.state = GearState.DOWN_LOCKED
            self.sensor.set_position(GearPosition.DOWN)
            self.log(f"GearState: {self.state.name}.")
            self.log(f"GearPosition: {self.sensor.get_position().name}")
        else:
            self.log("Invalid command rejected.")
            

    def command_gear_up(self):
        position = self.sensor.get_position()

        if position == GearPosition.UNKNOWN:
            self.fault = GearFault.SENSOR_MISMATCH
            self.log(f"Fault detected: {self.fault.name}")
            return

        if self.state == GearState.UP_LOCKED and position == GearPosition.UP:
            self.log(f"Command rejected:")
            self.log(f"GearState:{self.state.name}")
            self.log(f"GearPosition: {self.sensor.get_position().name}")
            return

        if self.state == GearState.DOWN_LOCKED and position == GearPosition.DOWN:
            self.state = GearState.TRANSITIONING_UP
            self.sensor.set_position(GearPosition.UNKNOWN)
            self.log(f"GearState: {self.state.name}.")
            time.sleep(1)
            self.state = GearState.UP_LOCKED
            self.sensor.set_position(GearPosition.UP)
            self.log(f"GearState: {self.state.name}.")
            self.log(f"GearPosition: {self.sensor.get_position().name}")
        else: 
            self.log("Invalid command rejected.")

    def command_reset_system(self):
        self.state = GearState.DOWN_LOCKED
        self.sensor.set_position(GearPosition.DOWN)
        self.fault = GearFault.NONE
        self.log(f"System reset:")
        self.log(f"GearState: {self.state.name}")
        self.log(f"GearPosition: {self.sensor.get_position().name}")
        self.log(f"FaultState: {self.fault.name}")

    def command_info(self):
        self.log("SYSTEM INFO:")
        self.log(f"State: {self.state.name}")
        self.log(f"Gear Position: {self.sensor.get_position().name}")
        self.log(f"Fault: {self.fault.name}")
    
    def command_shutdown(self):
        self.system_active = False
        self.log("System shutdown complete.")

def control_input(controller):
    while True:
        user_input = input("Enter command: up/down/reset/info/shutdown: \n")
        if user_input == "up":
            controller.receive_command(GearCommand.GEAR_UP)
        elif user_input == "down":
            controller.receive_command(GearCommand.GEAR_DOWN)
        elif user_input == "reset":
            controller.receive_command(GearCommand.RESET)
        elif user_input == "info":
            controller.receive_command(GearCommand.INFO)
        elif user_input == "shutdown":
            controller.receive_command(GearCommand.SHUTDOWN)
            return
        else:
            print("Please input a valid command.")

controller = LandingGearController()
control_input(controller)

