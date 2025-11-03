"""Just some user conversations funcs."""


def ask_for_continue() -> None:
    """Ask user to continue or break process via RuntimeError.

    Raises:
        RuntimeError: if user choised to break process.
    """
    ans = input("Continue? [Y/n] ").lower().strip()
    if ans and ans not in {"y", "yes"}:
        raise RuntimeError("Operation cancelled by user.") from None
        # Except it in entrypoint to show message and quit.
