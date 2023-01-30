#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demo Weather Station tango device server"""

import time

from tango import AttrQuality, AttrWriteType, DevState, DispLevel
from tango.server import Device, attribute, command, device_property, pipe


class WeatherStation(Device):

    windspeed = attribute(
        label="WindSpeed",
        dtype=float,
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ_WRITE,
        unit="km/hr",
        format="8.4f",
    )

    temperature = attribute(
        label="Temperature",
        dtype=float,
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ_WRITE,
        unit="K",
        format="8.4f",
        min_value=265,
        max_value=350,
        min_alarm=273,
        max_alarm=305,
        min_warning=260,
        max_warning=310,
        fget="get_temp",
        fset="set_temp",
    )

    ionization = attribute(
        label="Ionization",
        dtype=((int,),),
    )

    humidity = attribute(
        label="Humidity",
        dtype=((int,),),
    )

    info = pipe(label="Info")

    host = device_property(dtype=str)
    port = device_property(dtype=int, default_value=9788)

    def always_executed_hook(self):
        t = "Windspeed=%s Temperature=%s" % (self.windspeed, self.temperature)
        print(t)
        self.set_status(t)

    def init_device(self):
        Device.init_device(self)
        self.__windspeed = 0.0
        self.set_state(DevState.STANDBY)
        self.set_change_event("windspeed", True, False)

    def write_windspeed(self):
        self.info_stream("read_windspeed(%s, %d)", self.host, self.port)
        return 9.99, time.time(), AttrQuality.ATTR_WARNING

    def get_windspeed(self):
        self.info_stream("read windspeed %s", self.windspeed)
        return self.__windspeed

    def set_windspeed(self, windspeed):
        # should set the power supply current
        self.__windspeed = windspeed
        self.push_change_event("current", windspeed)

    def read_info(self):
        return "Information", dict(
            manufacturer="Tango", model="PS2000", version_number=123
        )

    # @DebugIt()
    # def read_noise(self):
    #     return numpy.random.random_integers(1000, size=(100, 100))

    @command
    def TurnOn(self):
        # turn on the actual power supply here
        # logging.info("Turning ON Power Supply")
        self.set_state(DevState.ON)

    @command
    def TurnOff(self):
        # turn off the actual power supply here
        self.set_state(DevState.OFF)

    # @command(dtype_in=float, doc_in="Ramp target current",
    #          dtype_out=bool, doc_out="True if ramping went well, "
    #          "False otherwise")
    # def Ramp(self, target_current):
    #     # should do the ramping
    #     return True


if __name__ == "__main__":
    WeatherStation.run_server()
