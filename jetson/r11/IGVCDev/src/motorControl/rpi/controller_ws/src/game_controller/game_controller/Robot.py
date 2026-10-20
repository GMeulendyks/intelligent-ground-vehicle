from inputs import get_gamepad
import math
import serial

# ser = serial.Serial(port="/dev/ttyACM0", baudrate=115200)

class Robot():
    def __init__(self, controller):
        self.controller = controller
        self.modes = ['Teleop', 'Autonomous_Forward', 'Autonomous_Waypoint']
        self.mode = 0
        # ser.write(b"begin 1000000")
        # ser.write(b"scan 10")
        print("Initial Operating Mode: " + str(self.modes[self.mode]))

    def switch_mode(self):
        self.mode += 1
        self.mode %= 3
        print("New mode is: " + str(self.modes[self.mode]))
    
    def on_pressed(self, button):
        match button:
            case 9:
                # self.switch_mode()
                # ser.write(b"wheel 1 200")
                pass
            # case 10:
                # ser.write(b"wheel 2 200")
            case default:
                pass
    
    # def on_released(self, button):
        # match button:
        #     case 9:
        #         # self.switch_mode()
        #         ser.write(b"wheel 1 0")
        #     case 10:
        #         ser.write(b"wheel 2 0")
        #     case default:
        #         pass
    
    def run(self):
        events = get_gamepad()
        for event in events:
            if event.state == 0:
                break
            self.on_pressed(event)


class XboxController():
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0



    def read(self): # return the buttons/triggers that you care about in this methode
        self._monitor_controller()
        x = self.X
        y = self.Y
        a = self.A
        b = self.B
        rb = self.RightBumper
        
        return [a, rb]


    def _monitor_controller(self):
        events = get_gamepad()
        for event in events:
            if event.code == 'ABS_Y':
                self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
            elif event.code == 'ABS_X':
                self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
            elif event.code == 'ABS_RY':
                self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
            elif event.code == 'ABS_RX':
                self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
            elif event.code == 'ABS_Z':
                self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
            elif event.code == 'ABS_RZ':
                self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
            elif event.code == 'BTN_TL':
                self.LeftBumper = event.state
            elif event.code == 'BTN_TR':
                self.RightBumper = event.state
            elif event.code == 'BTN_SOUTH':
                self.A = event.state
            elif event.code == 'BTN_NORTH':
                self.Y = event.state #previously switched with X
            elif event.code == 'BTN_WEST':
                self.X = event.state #previously switched with Y
            elif event.code == 'BTN_EAST':
                self.B = event.state
            elif event.code == 'BTN_THUMBL':
                self.LeftThumb = event.state
            elif event.code == 'BTN_THUMBR':
                self.RightThumb = event.state
            elif event.code == 'BTN_SELECT':
                self.Back = event.state
            elif event.code == 'BTN_START':
                self.Start = event.state
            elif event.code == 'BTN_TRIGGER_HAPPY1':
                self.LeftDPad = event.state
            elif event.code == 'BTN_TRIGGER_HAPPY2':
                self.RightDPad = event.state
            elif event.code == 'BTN_TRIGGER_HAPPY3':
                self.UpDPad = event.state
            elif event.code == 'BTN_TRIGGER_HAPPY4':
                self.DownDPad = event.state


# def main():
#     controller = XboxController()
#     robot = Robot(controller)
#     print("Initial Operating Mode: " + str(robot.modes[robot.mode]))
#     while True:
#         robot.run()


# if __name__ == '__main__':
#     main()