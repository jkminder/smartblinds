import signal
import logging
import threading

from pyhap.accessory import Bridge
from pyhap.accessory_driver import AccessoryDriver
import HAP.accessories

logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")

class HAP_Handler:
    """Handles all interaction with the apple home accessory protocol"""
    def __init__(self, bridge_name, persist_file = "HAP/hap_persistance.state"):
        self.driver = AccessoryDriver(port=51826, persist_file=persist_file)

        self.bridge = Bridge(self.driver, bridge_name)
        self.accessories = {}

        self._thread = None

    def add_accessory(self, accessorytype, accessoryname, localname):
        accessory = accessorytype(self.driver, accessoryname)
        self.bridge.add_accessory(accessory)
        self.accessories[accessoryname] = accessory

    def start(self):
        self.driver.add_accessory(accessory=self.bridge)

        self._thread = threading.Thread(target=self._driver_start)
        self._thread.start()

    def _driver_start(self):
        self.driver.start()

    def stop(self):
        self.driver.signal_handler(0, 0)






#initializing local hap handler
hap_handler = HAP_Handler("SmartBlinds")
hap_handler.add_accessory(HAP.accessories.smartblind_HAPaccessory, "Blinds Right", "right")
hap_handler.add_accessory(HAP.accessories.smartblind_HAPaccessory, "Blinds Left", "left")
hap_handler.accessories["Blinds Left"].local_target_listener = HAP.accessories.set_target_pos
hap_handler.accessories["Blinds Right"].local_target_listener = HAP.accessories.set_target_pos

