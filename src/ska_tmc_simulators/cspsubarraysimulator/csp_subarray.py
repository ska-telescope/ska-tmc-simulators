#!/usr/bin/env python
# Standard python import
"""Csp Subarray Module"""
import sys

from tango.server import run

# Additional import
from .utils import get_tango_server_class

# File generated on Mon Jul 12 13:24:36 2021 by tango-simlib-generator


def get_csp_subarray_simulator():
    """Returns CSP Subarray Simulator"""
    if len(sys.argv) > 0:
        device_name = sys.argv[1]
        if device_name.isdigit():
            device_name = f"mid-csp/subarray/{device_name}"
    else:
        device_name = "mid_csp_unset/elt/master"

    tango_ds = get_tango_server_class(device_name)
    return tango_ds[0]


def main(args=None, **kwargs):
    """
    Runs the CspSubarraySimulator.

    :param args: Arguments internal to TANGO
    :param kwargs: Arguments internal to TANGO

    :return: CspSubarraySimulator TANGO object.

    """
    cspsubarraysimulator = get_csp_subarray_simulator()
    ret_val = run((cspsubarraysimulator,), args=args, **kwargs)

    return ret_val


if __name__ == "__main__":
    main()
