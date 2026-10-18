"""Minimal ctypes access to the bundled HOMPACK shared library."""

import ctypes
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def _library_path() -> Path:
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

    return library_path


def load_library() -> ctypes.CDLL:
    """Load the HOMPACK shared library shipped next to this module."""
    library_path = _library_path()
    if sys.platform == "win32":
        compiler = shutil.which("gfortran")
        if compiler is not None:
            with os.add_dll_directory(str(Path(compiler).parent)):
                return ctypes.CDLL(str(library_path))

    return ctypes.CDLL(str(library_path))


def print_symbols() -> None:
    """Print the exported symbols in the HOMPACK shared library.

    Requires ``nm`` (Linux/macOS) or ``dumpbin``/GNU ``objdump`` (Windows).
    """
    library_path = _library_path()
    parse_objdump_exports = False

    if sys.platform == "win32":
        dumpbin = shutil.which("dumpbin")
        if dumpbin is not None:
            command = [dumpbin, "/exports", str(library_path)]
        else:
            objdump = shutil.which("objdump") or shutil.which(
                "x86_64-w64-mingw32-objdump"
            )
            if objdump is None:
                raise FileNotFoundError(
                    "print_symbols requires dumpbin or objdump on Windows"
                )
            command = [objdump, "-p", str(library_path)]
            parse_objdump_exports = True
    else:
        nm = shutil.which("nm") or shutil.which("llvm-nm")
        if nm is None:
            raise FileNotFoundError("print_symbols requires nm or llvm-nm")
        options = ["-gU"] if sys.platform == "darwin" else ["-D", "--defined-only"]
        command = [nm, *options, str(library_path)]

    result = subprocess.run(command, check=True, capture_output=True, text=True)
    if parse_objdump_exports:
        export_table = result.stdout.partition("[Ordinal/Name Pointer] Table")[2]
        symbols = re.findall(
            r"(?m)^\s*\[\s*\d+\]\s+\+base\[\s*\d+\]\s+[\da-fA-F]+\s+(\S+)",
            export_table,
        )
        print("\n".join(symbols))
        return

    print(result.stdout, end="")
