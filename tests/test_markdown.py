"""Tests for markdown utilities."""

import pytest

from claude_publish.markdown import extract_title


def test_extract_title(sample_markdown):
    assert extract_title(sample_markdown) == "My Test Post"


def test_extract_title_no_h1(sample_markdown_no_title):
    with pytest.raises(ValueError, match="No H1 title found"):
        extract_title(sample_markdown_no_title)


def test_extract_title_with_leading_spaces(tmp_path):
    md = tmp_path / "spaced.md"
    md.write_text("  # Spaced Title\n\nBody.\n")
    assert extract_title(md) == "Spaced Title"


def test_extract_title_ignores_h2(tmp_path):
    md = tmp_path / "h2first.md"
    md.write_text("## H2 First\n\n# Real Title\n")
    assert extract_title(md) == "Real Title"


def test_extract_title_first_h1_wins(tmp_path):
    md = tmp_path / "multi.md"
    md.write_text("# First\n\n# Second\n")
    assert extract_title(md) == "First"
