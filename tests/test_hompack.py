import hompack
from hompack._native import load_library


def test_version():
    """Check that the package version is available."""
    assert hompack.__version__ is not None


def test_native_library_loads():
    """Check that the native library can be loaded."""
    assert load_library()._handle
