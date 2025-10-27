"""Module to read excluded directories and files from configuration files."""

from core.settings.conf_reader import SETTINGS


PATH_TO_FILE_EXCLUDE_DIRS = SETTINGS["PATH_TO_FILE_EXCLUDE_DIRS"]
PATH_TO_FILE_EXCLUDE_FILES = SETTINGS["PATH_TO_FILE_EXCLUDE_FILES"]


def exclude_dirs(path=PATH_TO_FILE_EXCLUDE_DIRS):
    """Read exclude file and return list of excluded directories."""
    excluded_dirs = []
    try:
        with open(path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    excluded_dirs.append(line)
    except FileNotFoundError:
        pass  # If the file does not exist, return an empty list
    return excluded_dirs


def exclude_files(path=PATH_TO_FILE_EXCLUDE_FILES):
    """Read exclude file and return list of excluded files."""
    excluded_files = []
    try:
        with open(path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    excluded_files.append(line)
    except FileNotFoundError:
        pass  # If the file does not exist, return an empty list
    return excluded_files
