# -*- coding: utf-8 -*-
# pylint: disable=W0613
"""
override class with command handlers for CspMaster.
"""
# Standard python imports
import logging
from typing import Optional

from ska_tango_base.base.base_device import SKABaseDevice
from ska_tango_base.base.component_manager import BaseComponentManager
from ska_tango_base.commands import ResultCode
from ska_tango_base.control_model import HealthState
from tango import DevState
from tango.server import command, device_property, run

logger = logging.getLogger(__name__)


class EmptyComponentManager(BaseComponentManager):
    """Dummy Component Manager class"""

    def __init__(
        self, logger=None, max_workers: Optional[int] = None, *args, **kwargs
    ):
        super().__init__(
            logger=logger, max_workers=max_workers, *args, **kwargs
        )
        self._csp_master_fqdn = ""

    @property
    def csp_master_fqdn(self):
        """Csp Master Device FQDN getter"""
        return self._csp_master_fqdn

    @csp_master_fqdn.setter
    def csp_master_fqdn(self, value):
        """Csp Master Device FQDN setter"""
        self._csp_master_fqdn = value

    def start_communicating(self):
        """This method is not used by TMC."""
        self.logger.info("Start communicating method called")

    def stop_communicating(self):
        """This method is not used by TMC."""
        self.logger.info("Stop communicating method called")


class CspMasterDevice(SKABaseDevice):
    """Class for csp master simulator device"""

    CspMasterFQDN = device_property(dtype="str")

    def read_CspMasterFQDN(self):
        """Return the CspMasterFQDN attribute."""
        return self.component_manager.csp_master_fqdn

    def write_CspMasterFQDN(self, value):
        """Set the CspMasterFQDN attribute."""
        self.component_manager.csp_master_fqdn = value

    def init_device(self):
        super().init_device()
        self._health_state = HealthState.OK

    class InitCommand(SKABaseDevice.InitCommand):
        """Initializer class"""

        def do(self):
            """Do method during intialization"""
            super().do()
            self._device.set_change_event("State", True, False)
            self._device.set_change_event("healthState", True, False)
            return (ResultCode.OK, "")

    def create_component_manager(self):
        """Creates component manager"""
        cm = EmptyComponentManager(
            logger=self.logger,
            max_workers=None,
            communication_state_callback=None,
            component_state_callback=None,
        )
        return cm

    @command(
        dtype_in="DevState",
        doc_in="state to assign",
    )
    def SetDirectState(self, argin):
        """
        Trigger a DevState change
        """
        # import debugpy; debugpy.debug_this_thread()
        if self.dev_state() != argin:
            self.set_state(argin)
            self.push_change_event("State", self.dev_state())

    def is_On_allowed(self):
        """Command allowed method"""
        return True

    @command(
        dtype_in="DevVarStringArray",
        doc_in="Input argument as an empty list",
        dtype_out="DevVarLongStringArray",
        doc_out="(ReturnType, 'informational message')",
    )
    def On(self, argin):
        """On command method"""
        self.logger.info("Processing On command")
        if self.dev_state() != DevState.ON:
            self.set_state(DevState.ON)
            self.push_change_event("State", self.dev_state())
        return [[ResultCode.OK], [""]]

    def is_Off_allowed(self):
        """Command allowed method"""
        return True

    @command(
        dtype_in="DevVarStringArray",
        doc_in="Input argument as an empty list",
        dtype_out="DevVarLongStringArray",
        doc_out="(ReturnType, 'informational message')",
    )
    def Off(self, argin):
        """Off command method"""
        self.logger.info("Processing Off command")
        if self.dev_state() != DevState.OFF:
            self.set_state(DevState.OFF)
            self.push_change_event("State", self.dev_state())
        return [[ResultCode.OK], [""]]

    def is_Standby_allowed(self):
        """Command allowed method"""
        return True

    @command(
        dtype_in="DevVarStringArray",
        doc_in="Input argument as an empty list",
        dtype_out="DevVarLongStringArray",
        doc_out="(ReturnType, 'informational message')",
    )
    def Standby(self, argin):
        """Standby command method"""
        self.logger.info("Processing Standby command")
        if self.dev_state() != DevState.STANDBY:
            self.set_state(DevState.STANDBY)
            self.push_change_event("State", self.dev_state())
        return [[ResultCode.OK], [""]]

    @command(
        dtype_in=int,
        doc_in="state to assign",
    )
    def SetDirectHealthState(self, value):
        """
        Trigger a HealthState change
        """
        # import debugpy; debugpy.debug_this_thread()
        if self.healthState != value:
            self.healthState = value
            self.push_change_event("healthState", self.healthState)

    @property
    def healthState(self) -> HealthState:
        """Returns the healthstate of device"""
        return self._healthState

    @healthState.setter
    def healthState(self, value: HealthState) -> None:
        """Sets the healthState value for device"""
        self._healthState = value

    def set_health_state_degraded(self) -> list:
        """Sets the healthState to Degraded"""
        self.set_direct_healthstate(HealthState.DEGRADED)
        logger.info(
            "The healthState of device has changed to %s", self.healthState
        )
        if self.healthState == HealthState.DEGRADED:
            return [ResultCode.OK]
        return [ResultCode.FAILED]


def main(args=None, **kwargs):
    """
    Runs the CspMasterSimulator.

    :param args: Arguments internal to TANGO
    :param kwargs: Arguments internal to TANGO

    :return: CspMasterSimulator TANGO object.

    """
    return run((CspMasterDevice,), args=args, **kwargs)


if __name__ == "__main__":
    main()
