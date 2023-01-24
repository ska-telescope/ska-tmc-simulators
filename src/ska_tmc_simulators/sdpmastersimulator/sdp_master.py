#!/usr/bin/env python
# Standard python import
# Additional import
"""Sdp Master Module"""
from tango.server import run

from .utils import get_tango_server_class

# File generated on Mon Jul 12 13:24:36 2021 by tango-simlib-generator


def get_sdp_master_simulator():
    """Returns SDP Master Simulator"""
    device_name = "mid-sdp/control/0"
    tango_ds = get_tango_server_class(device_name)
    return tango_ds[0]


def main(args=None, **kwargs):
    """
    Runs the SdpMasterSimulator.

    :param args: Arguments internal to TANGO
    :param kwargs: Arguments internal to TANGO

    :return: SdpMasterSimulator TANGO object.

    """
    sdpmastersimulator = get_sdp_master_simulator()
    ret_val = run((sdpmastersimulator,), args=args, **kwargs)
    return ret_val


if __name__ == "__main__":
    main()
