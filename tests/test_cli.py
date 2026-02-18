"""Tests for trinity CLI — init command and E2E bootstrap flow."""

import json
import subprocess
import sys

import pytest


@pytest.fixture
def fresh_dir(tmp_path):
    """Provide a fresh temporary directory."""
    return tmp_path


class TestTrinityInit:
    """Test the 'trinity init' CLI command."""

    def test_creates_all_files(self, fresh_dir):
        """trinity init creates CLAUDE.md and .trinity/ with all three files."""
        result = subprocess.run(
            [sys.executable, "-m", "trinity_pattern.cli", "init", "--dir", str(fresh_dir)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

        assert (fresh_dir / "CLAUDE.md").exists()
        assert (fresh_dir / ".trinity" / "id.json").exists()
        assert (fresh_dir / ".trinity" / "local.json").exists()
        assert (fresh_dir / ".trinity" / "observations.json").exists()

    def test_id_json_has_correct_name_and_role(self, fresh_dir):
        """trinity init --name --role populates id.json correctly."""
        subprocess.run(
            [
                sys.executable,
                "-m",
                "trinity_pattern.cli",
                "init",
                "--dir",
                str(fresh_dir),
                "--name",
                "TestBot",
                "--role",
                "QA Engineer",
            ],
            capture_output=True,
            text=True,
        )

        with open(fresh_dir / ".trinity" / "id.json", encoding="utf-8") as f:
            data = json.load(f)

        assert data["identity"]["name"] == "TestBot"
        assert data["identity"]["role"] == "QA Engineer"
        assert data["trinity_version"] == "1.0.0"

    def test_does_not_overwrite_existing_files(self, fresh_dir):
        """Running trinity init twice doesn't overwrite existing files."""
        # First init
        subprocess.run(
            [
                sys.executable,
                "-m",
                "trinity_pattern.cli",
                "init",
                "--dir",
                str(fresh_dir),
                "--name",
                "First",
                "--role",
                "Original",
            ],
            capture_output=True,
            text=True,
        )

        # Second init with different name
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "trinity_pattern.cli",
                "init",
                "--dir",
                str(fresh_dir),
                "--name",
                "Second",
                "--role",
                "Override",
            ],
            capture_output=True,
            text=True,
        )

        # Original name should be preserved
        with open(fresh_dir / ".trinity" / "id.json", encoding="utf-8") as f:
            data = json.load(f)
        assert data["identity"]["name"] == "First"
        assert "Skipped" in result.stdout

    def test_claude_md_references_trinity_dir(self, fresh_dir):
        """Generated CLAUDE.md references .trinity/ directory."""
        subprocess.run(
            [sys.executable, "-m", "trinity_pattern.cli", "init", "--dir", str(fresh_dir)],
            capture_output=True,
            text=True,
        )

        content = (fresh_dir / "CLAUDE.md").read_text()
        assert ".trinity" in content
        assert "id.json" in content
        assert "local.json" in content
        assert "observations.json" in content

    def test_trinity_files_are_valid_json(self, fresh_dir):
        """All created .trinity/ files are valid JSON."""
        subprocess.run(
            [sys.executable, "-m", "trinity_pattern.cli", "init", "--dir", str(fresh_dir)],
            capture_output=True,
            text=True,
        )

        for filename in ["id.json", "local.json", "observations.json"]:
            with open(fresh_dir / ".trinity" / filename, encoding="utf-8") as f:
                data = json.load(f)  # Should not raise
            assert isinstance(data, dict)
            assert "trinity_version" in data


@pytest.mark.integration
class TestE2EBootstrap:
    """End-to-end tests verifying the full bootstrap flow."""

    def test_init_then_agent_loads_files(self, fresh_dir):
        """After init, Agent class can load the created files."""
        subprocess.run(
            [
                sys.executable,
                "-m",
                "trinity_pattern.cli",
                "init",
                "--dir",
                str(fresh_dir),
                "--name",
                "E2EBot",
                "--role",
                "Test Runner",
            ],
            capture_output=True,
            text=True,
        )

        # Verify Agent can load the initialized files
        from trinity_pattern import Agent

        agent = Agent(directory=str(fresh_dir / ".trinity"))
        context = agent.get_context()
        assert "E2EBot" in context
        assert "Test Runner" in context

    def test_init_then_session_roundtrip(self, fresh_dir):
        """After init, a full session can be recorded and persisted."""
        subprocess.run(
            [
                sys.executable,
                "-m",
                "trinity_pattern.cli",
                "init",
                "--dir",
                str(fresh_dir),
                "--name",
                "SessionBot",
                "--role",
                "Tester",
            ],
            capture_output=True,
            text=True,
        )

        from trinity_pattern import Agent

        agent = Agent(directory=str(fresh_dir / ".trinity"))
        agent.start_session()
        agent.log_activity("Ran E2E test")
        agent.add_learning("testing", "E2E bootstrap works")
        agent.end_session()

        # Reload and verify persistence
        agent2 = Agent(directory=str(fresh_dir / ".trinity"))
        context = agent2.get_context()
        assert "Ran E2E test" in context
        assert "testing" in context
