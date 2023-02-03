#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demo power supply tango device simulator"""

import logging

from ska_ser_logging import configure_logging
from tango import AttrWriteType, DevState, DispLevel
from tango.server import Device, attribute, command, device_property, run

configure_logging()
logger = logging.getLogger("ska.PowerSupply")


class PowerSupply(Device):

    """This is a Power Supply Device class."""

    temperature = attribute(
        label="temperature",
        dtype=float,
        display_level=DispLevel.EXPERT,
        access=AttrWriteType.READ_WRITE,
        unit="C",
        format="8.4f",
        min_value=-10.0,
        max_value=50.0,
        min_alarm=0.0,
        max_alarm=51.0,
        min_warning=0.0,
        max_warning=45.5,
        polling_period=1000,
        fget="get_temperature",
        fset="set_temperature",
        doc="the power supply temperature",
    )

    voltage = attribute(
        label="Voltage",
        dtype=float,
        display_level=DispLevel.EXPERT,
        access=AttrWriteType.READ_WRITE,
        unit="V",
        format="8.4f",
        min_value=5.0,
        max_value=12.0,
        min_alarm=5.0,
        max_alarm=13.0,
        min_warning=5.0,
        max_warning=12.5,
        polling_period=1000,
        fget="get_voltage",
        fset="set_voltage",
        doc="the power supply voltage",
    )

    current = attribute(
        label="Current",
        dtype=float,
        display_level=DispLevel.EXPERT,
        access=AttrWriteType.READ_WRITE,
        unit="A",
        format="8.4f",
        min_value=0.0,
        max_value=8.5,
        min_alarm=3.0,
        max_alarm=9.0,
        min_warning=3.5,
        max_warning=8.0,
        polling_period=1000,
        fget="get_current",
        fset="set_current",
        doc="the power supply current",
    )

    host = device_property(str, default_value="192.168.49.2")
    port = device_property(int, default_value=30005)

    def init_device(self):
        """Initialize power supply device."""
        Device.init_device(self)
        self.set_change_event("current", True, False)
        self.set_change_event("temperature", True, False)
        self.set_change_event("voltage", True, False)
        self.__current = 0.0
        self.__voltage = 0.0
        self.__temperature = 10.0
        self.set_state(DevState.STANDBY)
        logger.info("Power Supply Device Initialized")

    def get_current(self):
        """Read current of Power Supply Device."""
        return float(self.__current)

    def set_current(self, current):
        """Set current of Power Supply Device."""
        self.__current = current
        self.push_change_event("current", self.__current)

    def get_voltage(self):
        """Read voltage of Power Supply Device."""
        return self.__voltage

    def set_voltage(self, voltage):
        """Set voltage of Power Supply Device."""
        self.__voltage = voltage
        self.push_change_event("voltage", self.__voltage)

    def get_temperature(self):
        """Read temperature of Power Supply Device."""
        return self.__temperature

    def set_temperature(self, temperature):
        """Set temperature of Power Supply Device."""
        self.__temperature = temperature
        self.push_change_event("temperature", self.__temperature)

    @command
    def TurnOn(self):
        """Turn On Power Supply Device."""
        logger.info("Turning ON Power Supply.")
        self.set_state(DevState.ON)

    @command
    def TurnOff(self):
        """Turn Off Power Supply Device."""
        logger.info("Turning OFF Weather Station")
        self.set_state(DevState.OFF)

    @command(
        dtype_in=float,
        doc_in="Ramp target current",
        dtype_out=float,
        doc_out="Returns the Current set ",
    )
    def Ramp_current(self, target_current):
        """Ramp target current"""
        self.__current = target_current
        logger.info(f"Power Supply Device Current: {self.__current}")
        return self.__current

    @command(
        dtype_in=float,
        doc_in="Ramp target voltage",
        dtype_out=float,
        doc_out="Returns the voltage set. ",
    )
    def Ramp_voltage(self, target_voltage):
        """Ramp target voltage"""
        self.__voltage = target_voltage
        logger.info(f"Power Supply Device Voltage: {self.__voltage}")
        return self.__voltage


def main(args=None, **kwargs):
    """
    Runs the Power Supply Device simulator.

    :param args: Arguments internal to TANGO
    :param kwargs: Arguments internal to TANGO

    :return: PowerSupply TANGO object.

    """
    return run((PowerSupply,), args=args, **kwargs)


if __name__ == "__main__":
    main()
