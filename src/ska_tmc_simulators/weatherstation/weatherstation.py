#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demo Weather Station tango device server"""
import logging

from ska_ser_logging import configure_logging
from tango import AttrWriteType, DevState, DispLevel
from tango.server import Device, attribute, command, run

configure_logging()
logger = logging.getLogger("ska.WeatherStation")


class WeatherStation(Device):
    """This is weather station class"""

    def init_device(self):
        """Device init class"""
        Device.init_device(self)
        self.set_change_event("windspeed", True, False)
        self.set_change_event("temperature", True, False)
        self.set_change_event("ionization", True, False)
        self.set_change_event("humidity", True, False)
        self.__windspeed = 0.0
        self.__temperature = 0.0
        self.__ionization = 0.0
        self.__humidity = 0.0
        logger.info("Device initialized")

    windspeed = attribute(
        label="WindSpeed",
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        unit="m/s",
        fget="get_windspeed",
        fset="set_windspeed",
        format="8.4f",
    )

    temperature = attribute(
        label="Temperature",
        dtype=float,
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ_WRITE,
        fget="get_temperature",
        fset="set_temperature",
        unit="C",
        format="8.4f",
    )

    ionization = attribute(
        label="Ionization",
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        unit="mV",
        fget="get_ionization",
        fset="set_ionization",
    )

    humidity = attribute(
        label="Humidity",
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        unit="%",
        fget="get_humidity",
        fset="set_humidity",
    )

    def get_windspeed(self):
        """read windspeed"""
        return self.__windspeed

    def set_windspeed(self, value):
        """write windspeed"""
        self.__windspeed = value

    def get_temperature(self):
        """read temperature"""
        return self.__temperature

    def set_temperature(self, value):
        """write temperature"""
        self.__temperature = value

    def get_ionization(self):
        """read ionization"""
        return self.__ionization

    def set_ionization(self, value):
        """write ionization"""
        self.__ionization = value

    def get_humidity(self):
        """read humidity"""
        return self.__humidity

    def set_humidity(self, value):
        """write humidity"""
        self.__humidity = value

    @command
    def On(self):
        """Turn on Weather station"""

        logger.info("Turning ON Weather Station")
        self.set_state(DevState.ON)

    @command
    def Off(self):
        """Turn off Weather Station"""
        logger.info("Turning Off Weather Station")
        self.set_state(DevState.OFF)


def main(args=None, **kwargs):
    """Main function"""
    return run((WeatherStation,), args=args, **kwargs)


if __name__ == "__main__":
    main()
