"""NOTE! SETTINGS dict can be changed during programm running.
Key "TARGET_DIR" will be added from path = os.path.abspath(args.path)"""

import sys

from core.ansi.colorize import colorize


def __conf_read():
    """Configs in file must be like pairs:
    key1=value1
    key2=value2
    Config file must be [project root]/settings/config.conf
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    """
    with open("./settings/config.conf") as file:
        settings = {}
        for pair in file.readlines():
            k, v = pair.strip().split("=", 1)
            settings[k] = v
        print(colorize(sign="✓", code="32", text="Configuration loaded from ./settings/config.conf"))
        return settings
   
try:
    SETTINGS = __conf_read()
except Exception as e:
    print(str(e))
    print(__conf_read.__doc__)
    sys.exit(1)
