"""Integration tests for Trinity Pattern examples."""

import json
import os
import subprocess
import sys

import pytest

EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "examples")


@pytest.mark.integration
def test_claude_code_hook_produces_valid_output():
    """hook_inject.py must output valid JSON with output field."""
    result = subprocess.run(
        [sys.executable, os.path.join(EXAMPLES_DIR, "claude_code", "hook_inject.py")],
        capture_output=True,
        text=True,
        timeout=10,
        input='{"input": "test"}',
        env={**os.environ, "TRINITY_TEST_MODE": "1"},
    )
    assert result.returncode == 0, f"Exit code {result.returncode}: {result.stderr}"
    output = json.loads(result.stdout)
    assert "output" in output


@pytest.mark.integration
def test_chatgpt_context_generation():
    """generate_context.py must produce markdown context block."""
    result = subprocess.run(
        [sys.executable, os.path.join(EXAMPLES_DIR, "chatgpt", "generate_context.py")],
        capture_output=True,
        text=True,
        timeout=10,
        env={**os.environ, "TRINITY_TEST_MODE": "1"},
    )
    assert result.returncode == 0, f"Exit code {result.returncode}: {result.stderr}"
    assert len(result.stdout.strip()) > 0


@pytest.mark.integration
def test_generic_llm_api_prepend():
    """api_prepend.py must produce system prompt content."""
    result = subprocess.run(
        [sys.executable, os.path.join(EXAMPLES_DIR, "generic_llm", "api_prepend.py")],
        capture_output=True,
        text=True,
        timeout=10,
        env={**os.environ, "TRINITY_TEST_MODE": "1"},
    )
    assert result.returncode == 0, f"Exit code {result.returncode}: {result.stderr}"
    assert len(result.stdout.strip()) > 0
