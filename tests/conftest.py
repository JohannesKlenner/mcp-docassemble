"""Pytest configuration for MCP Docassemble tests."""

from __future__ import annotations

import os
from typing import Iterable

import pytest

_LIVE_TEST_ENV = "MCP_DOCASSEMBLE_LIVE_TESTS"
_SANITY_TEST_FILENAME = "test_sanity.py"


def pytest_collection_modifyitems(config: pytest.Config, items: Iterable[pytest.Item]) -> None:
    """Skip integration tests unless an explicit opt-in flag is provided.

    The existing test suite exercises a live Docassemble instance using
    stored credentials and therefore should never run in CI by default.
    Setting the ``MCP_DOCASSEMBLE_LIVE_TESTS`` environment variable to ``"1"``
    re-enables the tests for manual verification against a configured server.
    A lightweight sanity test always runs to validate the Python package
    without requiring external services.
    """
    if os.getenv(_LIVE_TEST_ENV) == "1":
        return

    skip_marker = pytest.mark.skip(reason="requires live Docassemble server; set MCP_DOCASSEMBLE_LIVE_TESTS=1 to enable")
    for item in items:
        if item.fspath.basename == _SANITY_TEST_FILENAME:
            continue
        item.add_marker(skip_marker)
