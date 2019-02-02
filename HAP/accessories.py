from pyhap.accessory import Accessory
import time
from pyhap.const import CATEGORY_SENSOR, CATEGORY_SWITCH, CATEGORY_FAN, CATEGORY_WINDOW_COVERING



class smartblind_HAPaccessory(Accessory):
    """Testversion of SmartBlinds"""
    category = CATEGORY_WINDOW_COVERING

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add the fan service. Also add optional characteristics to it.
        serv_blind = self.add_preload_service("WindowCovering")

        self.state = serv_blind.configure_char("PositionState")
        self.curr_pos = serv_blind.configure_char("CurrentPosition")
        self.target_pos = serv_blind.configure_char("TargetPosition", setter_callback=self.receive_target_pos)

        self.state.set_value(2) #set initial state to stopped
        self.send_target_pos(0) #send inital target position
        self.send_current_pos(0) #send initial current position
        self.local_target_listener = None

    def receive_target_pos(self, value):
        if (self.local_target_listener):
            self.local_target_listener(value)

    def send_current_pos(self, value):
        self.curr_pos.set_value(value)

    def send_target_pos(self, value):
        self.target_pos.set_value(value)




def set_target_pos(value):
   print("Setting TempLocalBlind to Position: ", value)
