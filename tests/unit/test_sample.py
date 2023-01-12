import pytest
from tango import DeviceProxy


@pytest.mark.unit
def test_csp_device():
    proxy = DeviceProxy("mid-csp/control/0")
    ping = proxy.ping()
    assert ping > 1
