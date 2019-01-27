"""An example of how to setup and start an Accessory.
This is:
1. Create the Accessory object you want.
2. Add it to an AccessoryDriver, which will advertise it on the local network,
    setup a server to answer client queries, etc.
"""
import logging
import signal
import random

from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
import pyhap.loader as loader
from pyhap import camera
from pyhap.const import CATEGORY_SENSOR, CATEGORY_SWITCH, CATEGORY_FAN

logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")

class Switch(Accessory):
    category = CATEGORY_SWITCH

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('Switch')
        self.char_temp = serv_temp.configure_char('CurrentSwitch')

class FakeFan(Accessory):
    """Fake Fan, only logs whatever the client set."""

    category = CATEGORY_FAN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add the fan service. Also add optional characteristics to it.
        serv_fan = self.add_preload_service(
            'Fan', chars=['RotationSpeed', 'RotationDirection'])

        self.char_rotation_speed = serv_fan.configure_char(
            'RotationSpeed', setter_callback=self.set_rotation_speed)
        self.char_rotation_direction = serv_fan.configure_char(
            'RotationDirection', setter_callback=self.set_rotation_direction)
        self.char_onoff = serv_fan.configure_char(
            "On", setter_callback=self.set_onstate)


    def set_rotation_speed(self, value):
        print("Rotation speed changed: %s", value)

    def set_rotation_direction(self, value):
        print("Rotation direction changed: %s", value)

    def set_onstate(self, value):
        if (value):
            print("Turned FakeFan On")
        else:
            print("Turned FakeFan Off")


class TemperatureSensor(Accessory):
    """Fake Temperature sensor, measuring every 3 seconds."""

    category = CATEGORY_SENSOR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('TemperatureSensor')
        self.char_temp = serv_temp.configure_char('CurrentTemperature')

    @Accessory.run_at_interval(3)
    async def run(self):
        self.char_temp.set_value(random.randint(18, 26))


def get_bridge(driver):
    """Call this method to get a Bridge instead of a standalone accessory."""
    bridge = Bridge(driver, 'Bridge')
    temp_sensor = TemperatureSensor(driver, 'TempSensor')
    fan = FakeFan(driver, 'Fan')
    bridge.add_accessory(temp_sensor)
    bridge.add_accessory(fan)

    return bridge


def get_accessory(driver):
    """Call this method to get a standalone Accessory."""
    return TemperatureSensor(driver, 'MyTempSensofr')


# Start the accessory on port 51826
driver = AccessoryDriver(port=51826, persist_file="accessory.state")


# Change `get_accessory` to `get_bridge` if you want to run a Bridge.
driver.add_accessory(accessory=get_bridge(driver))

# We want SIGTERM (terminate) to be handled by the driver itself,
# so that it can gracefully stop the accessory, server and advertising.
signal.signal(signal.SIGTERM, driver.signal_handler)

# Start it!
driver.start()
