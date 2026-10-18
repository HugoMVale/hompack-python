import hompack
from hompack._native import load_library


def test_version():
    assert hompack.__version__ is not None


def test_native_library_loads():
    assert load_library()._handle
