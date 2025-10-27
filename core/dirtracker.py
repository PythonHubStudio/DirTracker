"""
This module creates a "snapshot" of a directory (its full tree structure).
It detects any file changes since the last check, including:
- files that were added;
- files that were removed;
- files whose contents have changed, even by one byte.

The information about changes is printed to the terminal in the following format:

 - With full absolute paths (if `os.walk()` was run from an absolute path):
[+] New file: /home/user/course/app.py
[-] Removed file: /home/user/Documents/passport.pdf
[~] Changed file: /home/user/Documents/contacts.xlsx

 - Or with relative paths (if `os.walk()` was run from "."):
[+] New file: ./course/app.py
[-] Removed file: ./Documents/passport.pdf
[~] Changed file: ./Documents/contacts.xlsx
"""

import os
import pickle
import hashlib

from core.ansi.colorize import colorize
from core.settings.conf_reader import SETTINGS
from core.settings.exclude_reader import exclude_dirs, exclude_files


# Pickle file used to store the directory snapshot
SNAPSHOT_FILE = ".snapshot.pkl"  # Hidden file in the target directory (dot is not a mistake)
SNAPSHOT_PATH = os.path.join(SETTINGS.get("TARGET_DIR", "."), SNAPSHOT_FILE)


def hash_file(path: str | os.PathLike, *, chunk_size: int = 4096) -> str:
    """
    Return the MD5 hash of a file's contents.

    If the file cannot be read (deleted, locked, etc.), return an empty string.

    Args:
        path: Path to the file to hash.

    Returns:
        Hexadecimal MD5 hash string of the file contents.
    """
    md5 = hashlib.md5()

    with open(path, "rb") as file:
        while True:
            chunk = file.read(chunk_size)  # read in small pieces
            if not chunk:
                break
            md5.update(chunk)

        return md5.hexdigest()


def snapshot(
        directory: str | os.PathLike, *, interactive: bool = False
        ) -> dict[str, str]:
    """
    Create a snapshot (dictionary) of a directory state.

    The dictionary maps file paths to their MD5 hashes.

    Skips files that cannot be read or accessed.

    Args:
        directory: The directory path to scan.

    Returns:
        A dictionary {path: hash} for all files in the directory and subdirectories.
    """
    data: dict[str, str] = {}
    for root, dirs, files in os.walk(directory):
        # Exclude directories
        for ex_dir in exclude_dirs():
            if ex_dir in dirs:
                dirs.remove(ex_dir)

        # Exclude files
        for ex_file in exclude_files():
            if ex_file in files:
                files.remove(ex_file)

        for name in files:
            if name == SNAPSHOT_FILE:
                continue
            path = os.path.join(root, name)

            try:
                data[path] = hash_file(path)

            except PermissionError as e:
                print(colorize(sign="!", code="31", text=f"No access to {path!r}: {e}"))
                if interactive:
                    msg = "If you continue, the file will be considered deleted."
                    msg2 = "\nYou can try root access to run it."
                    print(colorize(sign="!", code="33", text=msg+msg2))
                    ans = input("Continue? [Y/n] ").lower().strip()
                    if ans and ans not in {"y", "yes"}:
                        raise RuntimeError("Operation cancelled by user.")
                        # Except it in entrypoint to show message and quit.
                continue

            except FileNotFoundError as e:
                print(colorize(sign="!", code="33", text=f"Skipping {path!r}: {e}"))
                print(colorize(sign="!", code="33", text=f"Maybe was deleted/renamed right now..."))
                continue

            except OSError as e:
                print(colorize(sign="!", code="31", text=f"OS error for {path!r}: {e}"))
                if interactive:
                    msg = "If you continue, the file will be considered deleted."
                    print(colorize(sign="!", code="33", text=msg))
                    ans = input("Continue? [Y/n] ").lower().strip()
                    if ans and ans not in {"y", "yes"}:
                        raise RuntimeError("Operation cancelled by user.")
                continue
    return data


def load_snapshot() -> dict[str, str]:
    """
    Load the saved snapshot from disk if it exists.

    Returns:
        A dictionary representing the previous snapshot state.
        Returns an empty dict if the snapshot file doesn't exist.
    """
    if os.path.exists(SNAPSHOT_PATH):
        try:
            with open(SNAPSHOT_PATH, "rb") as file:
                return pickle.load(file)
        except (EOFError, pickle.UnpicklingError):
            print(colorize(sign="!", code="31", text="Corrupted snapshot file. Recreating..."))
    return {}


def save_snapshot(new: dict[str, str]) -> None:
    with open(SNAPSHOT_PATH, "wb") as file:
        pickle.dump(new, file)



def watch(directory: str | os.PathLike = ".", *, interactive=False) -> None:
    """
    Compare the current directory state with the saved snapshot.

    It reports added, removed, and changed files, and then updates the snapshot file.

    Args:
        directory: The path to the directory to monitor (default is current directory).
    """
    abs_path = os.path.abspath(directory)
    print(f"Checking directory: {abs_path}")

    old = load_snapshot()
    new = snapshot(directory, interactive=interactive)

    if not old:
        save_snapshot(new)
        print(colorize(sign="✓", code="32", text="First snapshot was created!"))
        return

    added = new.keys() - old.keys()
    removed = old.keys() - new.keys()
    changed = set()
    for f in new.keys():
        if f in old.keys() and new[f] != old[f]:
            changed.add(f)

    if not (added or removed or changed):
        print(colorize(sign="✓", code="32", text="No changes detected."))
    else:
        for f in added:
            print(colorize(sign="+", code="32", text=f"New file: {f}"))
        for f in removed:
            print(colorize(sign="-", code="31", text=f"Removed file: {f}"))
        for f in changed:
            print(colorize(sign="~", code="33", text=f"Changed file: {f}"))

    save_snapshot(new)
