# !/usr/bin/env python
# Standard python import
"""Sdp Subarray Module"""
import sys

from tango.server import run

# Additional import
from .utils import get_tango_server_class

# File generated on Mon Jul 12 13:24:36 2021 by tango-simlib-generator


def get_sdp_subarray_simulator():
    """Returns SDP Subarray Simulator"""
    if len(sys.argv) > 0:
        device_name = sys.argv[1]
        if device_name.isdigit():
            device_name = f"mid-sdp/subarray/{device_name[1]}"
            # To omit 0 from name of device
    else:
        device_name = "mid_sdp_unset/elt/subarray_1"

    tango_ds = get_tango_server_class(device_name)
    return tango_ds[0]


def main(args=None, **kwargs):
    """
    Runs the SdpSubarraySimulator.

    :param args: Arguments internal to TANGO
    :param kwargs: Arguments internal to TANGO

    :return: SdpSubarraySimulator TANGO object.

    """
    sdpsubarraysimulator = get_sdp_subarray_simulator()
    ret_val = run((sdpsubarraysimulator,), args=args, **kwargs)

    return ret_val


if __name__ == "__main__":
    main()
