import pytest
import warnings
from tango import DeviceProxy

warnings.simplefilter(action='ignore', category=FutureWarning)

@pytest.mark.temp
def test_ping():
    proxy = DeviceProxy("mid-csp/control/0")
    ping = proxy.ping()
    assert ping > 1
