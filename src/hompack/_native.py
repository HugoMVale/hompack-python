"""Minimal ctypes access to the bundled HOMPACK shared library."""

import ctypes
import os
import shutil
import sys
from pathlib import Path


def load_library() -> ctypes.CDLL:
    """Load the HOMPACK shared library shipped next to this module."""
    if sys.platform == "win32":
        library_name = "hompack.dll"
    elif sys.platform == "darwin":
        library_name = "libhompack.dylib"
    else:
        library_name = "libhompack.so"

    library_path = Path(__file__).with_name(library_name)
    if not library_path.is_file():
        build_dir = Path(__file__).resolve().parents[2] / "build"
        build_libraries = sorted(build_dir.glob(f"*/{library_name}"))
        if not build_libraries:
            raise FileNotFoundError(f"Could not find the HOMPACK library: {library_name}")
        library_path = build_libraries[0]

    if sys.platform == "win32":
        compiler = shutil.which("gfortran")
        if compiler is not None:
            with os.add_dll_directory(str(Path(compiler).parent)):
                return ctypes.CDLL(str(library_path))

    return ctypes.CDLL(str(library_path))