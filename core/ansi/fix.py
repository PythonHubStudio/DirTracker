"""It fix ANSI color support in the Windows console.
If you dont know about ctypes module, you are definitely lucky!
You don't need to know that... Keep save your neurons, I'm serious."""

import os
import ctypes


def enable_ansi_colors() -> None:
    """
    Enables ANSI color support in the Windows console (if needed).
    On other systems (Linux, macOS), this function does nothing.
    """

    if os.name != "nt":
        return  # Non-Windows systems already support ANSI.

    # Get handle for standard output.
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE = -11.

    # Get current console mode.
    mode = ctypes.c_uint()
    if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
        return

    # Enable ANSI escape sequences.
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    new_mode = mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
    kernel32.SetConsoleMode(handle, new_mode)


if __name__ == "__main__":
    enable_ansi_colors()

    # Test
    print("\033[1;32mGreen text\033[0m normal text")
    print("\033[1;31mRed text\033[0m normal text")
    print("\033[1;33mYellow text\033[0m normal text")
