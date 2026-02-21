"""Tests for trinity CLI — init command and E2E bootstrap flow."""

import json
import subprocess
from pathlib import Path
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

    def test_agents_md_created(self, fresh_dir):
        """trinity init creates AGENTS.md file."""
        result = subprocess.run(
            [sys.executable, "-m", "trinity_pattern.cli", "init", "--dir", str(fresh_dir)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert (fresh_dir / "AGENTS.md").exists()

    def test_agents_md_content(self, fresh_dir):
        """Generated AGENTS.md contains key Trinity Pattern content."""
        subprocess.run(
            [sys.executable, "-m", "trinity_pattern.cli", "init", "--dir", str(fresh_dir)],
            capture_output=True,
            text=True,
        )

        content = (fresh_dir / "AGENTS.md").read_text()
        assert "trinity_pattern" in content
        assert "Agent" in content
        assert ".trinity" in content
        assert "id.json" in content
        assert "local.json" in content
        assert "observations.json" in content

    def test_agents_md_skip_existing(self, fresh_dir):
        """trinity init does not overwrite existing AGENTS.md."""
        # Create a custom AGENTS.md first
        custom_content = "# Custom AGENTS.md — do not overwrite"
        (fresh_dir / "AGENTS.md").write_text(custom_content)

        result = subprocess.run(
            [sys.executable, "-m", "trinity_pattern.cli", "init", "--dir", str(fresh_dir)],
            capture_output=True,
            text=True,
        )

        # Original content should be preserved
        assert (fresh_dir / "AGENTS.md").read_text() == custom_content
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


class TestCLIDirect:
    """Direct-import tests for cli.py to enable coverage instrumentation.

    The subprocess-based tests above cannot measure coverage of cli.py because
    coverage only instruments the current process. These tests import and call
    CLI functions directly so coverage can track execution.
    """

    def test_get_template_path_returns_path(self):
        """_get_template_path() returns a Path object pointing to templates/CLAUDE.md."""
        from trinity_pattern.cli import _get_template_path

        result = _get_template_path()
        assert isinstance(result, Path)
        assert result.name == "CLAUDE.md"
        assert "templates" in result.parts

    def test_get_agents_template_path_returns_path(self):
        """_get_agents_template_path() returns a Path pointing to templates/AGENTS.md."""
        from trinity_pattern.cli import _get_agents_template_path

        result = _get_agents_template_path()
        assert isinstance(result, Path)
        assert result.name == "AGENTS.md"
        assert "templates" in result.parts

    def test_cmd_init_creates_files(self, tmp_path):
        """cmd_init() creates all Trinity files when called directly."""
        import argparse

        from trinity_pattern.cli import cmd_init

        args = argparse.Namespace(
            dir=str(tmp_path),
            name="DirectBot",
            role="Tester",
        )
        cmd_init(args)

        assert (tmp_path / ".trinity" / "id.json").exists()
        assert (tmp_path / ".trinity" / "local.json").exists()
        assert (tmp_path / ".trinity" / "observations.json").exists()
        assert (tmp_path / "CLAUDE.md").exists()
        assert (tmp_path / "AGENTS.md").exists()

        with open(tmp_path / ".trinity" / "id.json", encoding="utf-8") as f:
            data = json.load(f)
        assert data["identity"]["name"] == "DirectBot"
        assert data["identity"]["role"] == "Tester"

    def test_cmd_init_skips_existing(self, tmp_path):
        """cmd_init() skips files that already exist."""
        import argparse

        from trinity_pattern.cli import cmd_init

        # First init
        args = argparse.Namespace(dir=str(tmp_path), name="First", role="Original")
        cmd_init(args)

        # Second init — should skip all
        args2 = argparse.Namespace(dir=str(tmp_path), name="Second", role="Override")
        cmd_init(args2)

        with open(tmp_path / ".trinity" / "id.json", encoding="utf-8") as f:
            data = json.load(f)
        assert data["identity"]["name"] == "First"

    def test_main_no_command_exits_1(self):
        """main() with no command prints help and exits with code 1."""
        import unittest.mock

        from trinity_pattern.cli import main

        with unittest.mock.patch("sys.argv", ["trinity"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    def test_main_init_command(self, tmp_path):
        """main() with 'init' command runs successfully."""
        import unittest.mock

        from trinity_pattern.cli import main

        with unittest.mock.patch(
            "sys.argv",
            ["trinity", "init", "--dir", str(tmp_path), "--name", "CLIBot", "--role", "Bot"],
        ):
            main()

        assert (tmp_path / ".trinity" / "id.json").exists()

    def test_cmd_init_missing_templates(self, tmp_path):
        """cmd_init() handles missing templates gracefully."""
        import argparse
        import unittest.mock

        from trinity_pattern.cli import cmd_init

        args = argparse.Namespace(dir=str(tmp_path), name="NoTemplate", role="Tester")

        # Mock template paths to non-existent locations
        fake_path = Path("/tmp/nonexistent/CLAUDE.md")
        fake_agents_path = Path("/tmp/nonexistent/AGENTS.md")

        with unittest.mock.patch(
            "trinity_pattern.cli._get_template_path", return_value=fake_path
        ), unittest.mock.patch(
            "trinity_pattern.cli._get_agents_template_path", return_value=fake_agents_path
        ):
            cmd_init(args)

        # Trinity JSON files should still be created
        assert (tmp_path / ".trinity" / "id.json").exists()
        assert (tmp_path / ".trinity" / "local.json").exists()
        assert (tmp_path / ".trinity" / "observations.json").exists()
        # But CLAUDE.md and AGENTS.md should not exist (templates were missing)
        assert not (tmp_path / "CLAUDE.md").exists()
        assert not (tmp_path / "AGENTS.md").exists()

    def test_cmd_init_nothing_to_do(self, tmp_path, capsys):
        """cmd_init() prints 'Nothing to do' when all files exist but no new ones created."""
        import argparse

        from trinity_pattern.cli import cmd_init

        # First init to create everything
        args = argparse.Namespace(dir=str(tmp_path), name="Bot", role="Tester")
        cmd_init(args)

        # Clear output
        capsys.readouterr()

        # Second init — everything already exists
        args2 = argparse.Namespace(dir=str(tmp_path), name="Bot2", role="Tester2")
        cmd_init(args2)

        captured = capsys.readouterr()
        assert "Skipped" in captured.out
