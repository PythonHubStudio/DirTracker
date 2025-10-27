import sys


USE_COLOR = sys.stdout.isatty()  # True → terminal, False → redirected output


def colorize(*, sign: str, code: str, text: str) -> str:
    """Return text wrapped in ANSI color codes if allowed."""
    if not USE_COLOR:
        return f"[{sign}] " + text

    return f"[\033[1;{code}m{sign}\033[0m] \033[1;{code}m{text}\033[0m"
