import os
from pathlib import Path
from typing import Iterable, Optional

DEFAULT_CONFIG_FILENAMES: tuple[str, ...] = (
    "hyperion.ini",
    "hyperion.conf",
    "hyperion.cfg",
    "hyperion.json",
    "hyperion.yml",
    "hyperion.yaml",
)

DEFAULT_CONFIG_CHILD_DIRS: tuple[str, ...] = ("config",)


def iter_default_config_candidates(cwd: Path) -> Iterable[Path]:
    """
    Yield default config candidates in deterministic lookup order:

      1) <cwd>/<filename> for each DEFAULT_CONFIG_FILENAMES (in order)
      2) <cwd>/config/<filename> for each DEFAULT_CONFIG_FILENAMES (in order)
    """
    # Step 1: PWD
    for filename in DEFAULT_CONFIG_FILENAMES:
        yield cwd / filename

    # Step 2: child dirs (currently only "config")
    for child_dir in DEFAULT_CONFIG_CHILD_DIRS:
        root = cwd / child_dir
        for filename in DEFAULT_CONFIG_FILENAMES:
            yield root / filename


def find_default_config_file(cwd: Path = Path(os.getcwd())) -> Optional[Path]:
    """
    Return the first existing default config file according to deterministic
    lookup rules, or None if nothing is found.
    """
    for candidate in iter_default_config_candidates(cwd):
        if candidate.is_file():
            return candidate
    return None
