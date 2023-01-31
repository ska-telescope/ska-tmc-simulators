#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demo Weather Station tango device server"""
import logging

from tango import AttrWriteType, DevState, DispLevel
from tango.server import Device, attribute, command, run


class WeatherStation(Device):
    """This is weather station class"""

    def init_device(self):
        """Device init class"""
        logging.info("device initialized")
        self.windspeed = 0.0
        self.temperature = 0.0
        self.ionization = 0.0
        self.humidity = 0.0

    windspeed = attribute(
        label="WindSpeed",
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        unit="m/s",
        format="8.4f",
    )

    temperature = attribute(
        label="Temperature",
        dtype=float,
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ_WRITE,
        unit="C",
        format="8.4f",
    )

    ionization = attribute(
        label="Ionization",
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        unit="mV",
    )

    humidity = attribute(
        label="Humidity",
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        unit="%",
    )

    def read_windspeed(self):
        """read windspeed"""
        return self.windspeed

    def write_windspeed(self, value):
        """write windspeed"""
        self.windspeed = value

    def read_temperature(self):
        """read temperature"""
        return self.temperature

    def write_temperature(self, value):
        """write temperature"""
        self.temperature = value

    def read_ionization(self):
        """read ionization"""
        return self.ionization

    def write_ionization(self, value):
        """write ionization"""
        self.ionization = value

    def read_humidity(self):
        """read humidity"""
        return self.humidity

    def write_humidity(self, value):
        """write humidity"""
        self.humidity = value

    @command
    def TurnOn(self):
        """Turn on actual power supply"""
        # turn on the actual power supply here
        # logging.info("Turning ON Power Supply")
        self.set_state(DevState.ON)

    @command
    def TurnOff(self):
        """Turn off actual power supply"""
        # turn off the actual power supply here
        self.set_state(DevState.OFF)


def main(args=None, **kwargs):
    """Main function"""
    return run((WeatherStation,), args=args, **kwargs)


if __name__ == "__main__":
    main()
