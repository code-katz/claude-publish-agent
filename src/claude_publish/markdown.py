"""Markdown utilities."""

from pathlib import Path


def extract_title(filepath: Path) -> str:
    """Extract the title from the first H1 line in a markdown file.

    Raises ValueError if no H1 is found.
    """
    with open(filepath) as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("# ") and not stripped.startswith("## "):
                return stripped[2:].strip()

    raise ValueError(
        f"No H1 title found in {filepath}. "
        "The file must contain a '# Title' line."
    )
