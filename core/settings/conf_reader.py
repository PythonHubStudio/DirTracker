"""NOTE! SETTINGS dict can be changed during programm running.
Key "TARGET_DIR" will be added from path = os.path.abspath(args.path)"""

import os
import sys

from core.ansi.colorize import colorize


def __conf_read() -> dict[str, str | os.PathLike[str]]:
    """Configs in file must be like pairs:
    key1=value1
    key2=value2
    Config file must be [project root]/settings/config.conf
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    """
    with open("./settings/config.conf") as file:
        settings: dict[str, str | os.PathLike[str]] = {}
        for pair in file.readlines():
            pair = pair.strip()
            if pair.startswith("#") or not pair:
                continue
            k, v = pair.split("=", 1)
            settings[k] = v
            msg = "Configuration loaded from ./settings/config.conf"
        print(colorize(sign="✓", code="32", text=msg))
        return settings


try:
    SETTINGS = __conf_read()
except Exception as e:
    print(str(e))
    print(__conf_read.__doc__)
    sys.exit(1)
