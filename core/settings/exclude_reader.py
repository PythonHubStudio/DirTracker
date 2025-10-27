"""Module to read excluded directories and files from configuration files."""

import os
from core.settings.conf_reader import SETTINGS


PATH_TO_FILE_EXCLUDE_DIRS = SETTINGS["PATH_TO_FILE_EXCLUDE_DIRS"]
PATH_TO_FILE_EXCLUDE_FILES = SETTINGS["PATH_TO_FILE_EXCLUDE_FILES"]


def exclude_dirs(
    path: str | os.PathLike[str] = PATH_TO_FILE_EXCLUDE_DIRS,
) -> list[str]:
    """Read exclude file and return list of excluded directories."""
    excluded_dirs: list[str] = []
    try:
        with open(path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    excluded_dirs.append(line)
    except FileNotFoundError:
        pass  # If the file does not exist, return an empty list
    return excluded_dirs


def exclude_files(
    path: str | os.PathLike[str] = PATH_TO_FILE_EXCLUDE_FILES,
) -> list[str]:
    """Read exclude file and return list of excluded files."""
    excluded_files: list[str] = []
    try:
        with open(path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    excluded_files.append(line)
    except FileNotFoundError:
        pass  # If the file does not exist, return an empty list
    return excluded_files
