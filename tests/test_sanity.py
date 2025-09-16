"""Lightweight unit tests that are safe to run in CI."""

from mcp_docassemble.client import DocassembleClient


def test_client_initialization():
    client = DocassembleClient(base_url="https://example.com", api_key="dummy")
    assert client.base_url == "https://example.com"
    assert client.api_key == "dummy"
