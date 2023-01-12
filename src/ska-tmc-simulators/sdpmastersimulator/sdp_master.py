#!/usr/bin/env python
# Standard python import
# Additional import
from .utils import get_tango_server_class
from tango.server import run

# File generated on Mon Jul 12 13:24:36 2021 by tango-simlib-generator


def get_sdp_master_simulator():
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
    SdpMasterSimulator = get_sdp_master_simulator()
    ret_val = run((SdpMasterSimulator,), args=args, **kwargs)
    return ret_val

if __name__ == "__main__":
    main()