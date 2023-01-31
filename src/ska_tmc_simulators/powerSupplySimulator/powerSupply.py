#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demo power supply tango device simulator"""

import numpy
from tango import AttrWriteType, DebugIt, DevState, DispLevel
from tango.server import Device, attribute, command, device_property, pipe, run


class PowerSupply(Device):

    temperature = attribute(
        label="temperature",
        dtype=float,
        display_level=DispLevel.EXPERT,
        access=AttrWriteType.READ_WRITE,
        unit="C",
        format="8.4f",
        min_value=20.0,
        max_value=50.0,
        min_alarm=10.0,
        max_alarm=50.0,
        min_warning=10.0,
        max_warning=50.5,
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
        max_value=8.5,
        min_alarm=5.0,
        max_alarm=8.5,
        min_warning=5.0,
        max_warning=8.5,
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
        min_alarm=0.1,
        max_alarm=8.4,
        min_warning=0.5,
        max_warning=8.0,
        polling_period=1000,
        fget="get_current",
        fset="set_current",
        doc="the power supply current",
    )

    noise = attribute(
        label="Noise", dtype=((int,),), max_dim_x=1024, max_dim_y=1024
    )

    info = pipe(label="Info")

    host = device_property(str, default_value="192.168.49.2")
    port = device_property(int, default_value=30005)

    def init_device(self):
        Device.init_device(self)
        self.set_change_event("voltage", True, False)
        self.set_change_event("current", True, False)
        self.set_change_event("temperature", True, False)
        self.__current = 0.0
        self.__voltage = 0.0
        self.__temperature = 10.0
        self.set_state(DevState.STANDBY)

    def get_current(self):
        return float(self.__current)

    def set_current(self, current):
        # should set the power supply current
        self.__current = current

    def get_voltage(self):
        return self.__voltage

    def set_voltage(self, voltage):
        # should set the power supply current
        self.__voltage = voltage

    def get_temperature(self):
        return self.__temperature

    def set_temperature(self, temperature):
        # should set the power supply current
        self.__temperature = temperature

    def read_info(self):
        return "Information", dict(
            manufacturer="SKA-TMC-HIMALAYA",
            model="HIM-1000",
            version_number=123,
        )

    @DebugIt()
    def read_noise(self):
        return numpy.random.random_integers(1000, size=(100, 100))

    @command
    def TurnOn(self):
        # turn on the actual power supply here
        self.set_state(DevState.ON)

    @command
    def TurnOff(self):
        # turn off the actual power supply here
        self.set_state(DevState.OFF)

    @command(
        dtype_in=float,
        doc_in="Ramp target current",
        dtype_out=float,
        doc_out="Returns the Current set ",
    )
    def Ramp_current(self, target_current):
        # set power supply current
        self.__current = target_current
        return self.__current

    @command(
        dtype_in=float,
        doc_in="Ramp target voltage",
        dtype_out=float,
        doc_out="Returns the voltage set. ",
    )
    def Ramp_voltage(self, target_voltage):
        # set power supply voltage
        self.__voltage = target_voltage
        return self.__voltage

    @command(
        dtype_in=float,
        doc_in="Ramp target temperature",
        dtype_out=float,
        doc_out="Returns the temperature set. ",
    )
    def Ramp_temperature(self, target_temperature):
        # set power supply temperature
        self.__temperature = target_temperature
        return self.__temperature


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
