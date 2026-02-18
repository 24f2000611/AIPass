"""Tests for the Trinity Pattern Agent class."""

import json

import pytest

from trinity_pattern import Agent


@pytest.fixture
def agent(tmp_path):
    """Create an agent in a temporary directory."""
    return Agent(
        directory=str(tmp_path / "test_agent"),
        name="TestBot",
        role="Test Assistant",
        platform="generic",
    )


class TestInit:
    def test_creates_directory(self, agent):
        assert agent.directory.exists()

    def test_creates_id_file(self, agent):
        assert agent._id_path.exists()
        data = json.loads(agent._id_path.read_text())
        assert data["trinity_version"] == "1.0.0"
        assert data["identity"]["name"] == "TestBot"
        assert data["identity"]["role"] == "Test Assistant"

    def test_creates_local_file(self, agent):
        assert agent._local_path.exists()
        data = json.loads(agent._local_path.read_text())
        assert data["trinity_version"] == "1.0.0"
        assert data["config"]["max_lines"] == 600
        assert data["sessions"] == []

    def test_creates_observations_file(self, agent):
        assert agent._observations_path.exists()
        data = json.loads(agent._observations_path.read_text())
        assert data["trinity_version"] == "1.0.0"
        assert data["observations"] == []

    def test_loads_existing_files(self, tmp_path):
        """Agent should load existing files rather than overwrite."""
        agent_dir = tmp_path / "existing_agent"
        agent1 = Agent(directory=str(agent_dir), name="First", role="Role1")
        agent1.start_session()
        agent1.log_activity("did something")
        agent1.end_session()

        agent2 = Agent(directory=str(agent_dir), name="Second", role="Role2")
        assert agent2._id["identity"]["name"] == "First"
        assert len(agent2._local["sessions"]) == 1


class TestSession:
    def test_start_session(self, agent):
        num = agent.start_session()
        assert num == 1
        assert agent._session_active is True
        assert len(agent._local["sessions"]) == 1

    def test_sequential_sessions(self, agent):
        agent.start_session()
        agent.end_session()
        num = agent.start_session()
        assert num == 2

    def test_log_activity(self, agent):
        agent.start_session()
        agent.log_activity("Built a feature")
        assert "Built a feature" in agent._current_session["activities"]

    def test_log_activity_without_session_raises(self, agent):
        with pytest.raises(RuntimeError, match="No active session"):
            agent.log_activity("Should fail")

    def test_end_session(self, agent):
        agent.start_session()
        agent.log_activity("Task A")
        agent.end_session()
        assert agent._session_active is False
        assert agent._local["sessions"][-1]["status"] == "completed"
        assert "Task A" in agent._local["active"]["recently_completed"]

    def test_end_session_without_start_raises(self, agent):
        with pytest.raises(RuntimeError, match="No active session"):
            agent.end_session()

    def test_recently_completed_max_20(self, agent):
        for i in range(25):
            agent.start_session()
            agent.log_activity(f"task_{i}")
            agent.end_session()
        assert len(agent._local["active"]["recently_completed"]) == 20


class TestLearnings:
    def test_add_learning(self, agent):
        agent.add_learning("test_key", "test_value")
        assert "test_key" in agent._local["key_learnings"]
        assert "test_value" in agent._local["key_learnings"]["test_key"]

    def test_learning_has_timestamp(self, agent):
        agent.add_learning("key", "value")
        entry = agent._local["key_learnings"]["key"]
        assert "[" in entry and "]" in entry


class TestObserve:
    def test_observe_creates_entry(self, agent):
        agent.observe("User prefers short answers", tags=["communication"])
        assert len(agent._observations["observations"]) == 1
        entry = agent._observations["observations"][0]["entries"][0]
        assert entry["observation"] == "User prefers short answers"
        assert "communication" in entry["tags"]

    def test_observe_default_tags(self, agent):
        agent.observe("No tags observation")
        entry = agent._observations["observations"][0]["entries"][0]
        assert entry["tags"] == []

    def test_observe_groups_by_date(self, agent):
        agent.observe("First observation")
        agent.observe("Second observation")
        assert len(agent._observations["observations"]) == 1
        assert len(agent._observations["observations"][0]["entries"]) == 2


class TestGetContext:
    def test_returns_string(self, agent):
        ctx = agent.get_context()
        assert isinstance(ctx, str)

    def test_includes_identity(self, agent):
        ctx = agent.get_context()
        assert "TestBot" in ctx
        assert "Test Assistant" in ctx

    def test_includes_sessions(self, agent):
        agent.start_session()
        agent.log_activity("Reviewed code")
        agent.end_session()
        ctx = agent.get_context()
        assert "Reviewed code" in ctx

    def test_includes_learnings(self, agent):
        agent.add_learning("pattern", "Always test first")
        ctx = agent.get_context()
        assert "pattern" in ctx
        assert "Always test first" in ctx

    def test_includes_observations(self, agent):
        agent.observe("User likes brevity", tags=["style"])
        ctx = agent.get_context()
        assert "User likes brevity" in ctx


class TestRollover:
    def test_needs_rollover_false_initially(self, agent):
        assert agent.needs_rollover() is False

    def test_needs_rollover_true_when_exceeded(self, agent):
        agent._local["metadata"]["current_lines"] = 700
        assert agent.needs_rollover() is True

    def test_rollover_extracts_sessions(self, agent):
        for i in range(10):
            agent.start_session()
            agent.log_activity(f"session_{i}_work")
            agent.end_session()

        before_count = len(agent._local["sessions"])
        extracted = agent.rollover()
        after_count = len(agent._local["sessions"])

        assert len(extracted) == before_count // 2
        assert after_count == before_count - len(extracted)

    def test_rollover_records_history(self, agent):
        agent.start_session()
        agent.log_activity("work")
        agent.end_session()
        agent.rollover()

        history = agent._local["metadata"]["rollover_history"]
        assert len(history) == 1
        assert "sessions_extracted" in history[0]

    def test_rollover_empty_sessions(self, agent):
        extracted = agent.rollover()
        assert extracted == []


class TestPersistence:
    def test_data_persists_to_disk(self, tmp_path):
        agent_dir = str(tmp_path / "persist_test")
        agent = Agent(directory=agent_dir, name="Persist", role="Tester")
        agent.start_session()
        agent.log_activity("Persisted work")
        agent.add_learning("persistence", "It works")
        agent.observe("Testing persistence", tags=["test"])
        agent.end_session()

        local = json.loads((tmp_path / "persist_test" / "local.json").read_text())
        assert len(local["sessions"]) == 1
        assert "persistence" in local["key_learnings"]

        obs = json.loads((tmp_path / "persist_test" / "observations.json").read_text())
        assert len(obs["observations"]) == 1
