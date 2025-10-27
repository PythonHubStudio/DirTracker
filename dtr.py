import os
import sys
import argparse

from core.settings.conf_reader import SETTINGS  # dict from ./settings/config.conf
from core.ansi.fix import enable_ansi_colors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Watch for file changes in a directory. *Supports redirecting std."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=SETTINGS.get("PATH"),
        help="Path to dir you want to follow. Default is CWD"
    )

    args = parser.parse_args()

    path = os.path.abspath(args.path)

    if not os.path.isdir(path):
        parser.error(f"Its not a dir: {path}")

    if os.name == "nt" and sys.stdout.isatty():
        enable_ansi_colors()

    SETTINGS["TARGET_DIR"] = path

    from core.dirtracker import watch  # !SETTINGS MUST BE READY!
    watch(path, interactive=True)


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(str(e))

