"""Trinity Pattern — Agent class for persistent AI identity."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .schemas import default_id, default_local, default_observations


class Agent:
    """Manages Trinity Pattern files for an AI agent.

    Three files define an agent's persistent identity:
    - id.json: Who the agent is (permanent)
    - local.json: What the agent has done (rolling session history)
    - observations.json: How the agent collaborates (rolling patterns)
    """

    def __init__(
        self,
        directory: str,
        name: str = "Agent",
        role: str = "AI Assistant",
        platform: str = "generic",
    ):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

        self._id_path = self.directory / "id.json"
        self._local_path = self.directory / "local.json"
        self._observations_path = self.directory / "observations.json"

        self._id = self._load_or_create(self._id_path, lambda: default_id(name, role, platform))
        self._local = self._load_or_create(self._local_path, default_local)
        self._observations = self._load_or_create(self._observations_path, default_observations)

        self._session_active = False
        self._current_session = None

    def _load_or_create(self, path: Path, factory) -> dict:
        """Load a JSON file or create it from a factory function."""
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        data = factory()
        self._save(path, data)
        return data

    def _save(self, path: Path, data: dict) -> None:
        """Write data to a JSON file."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")

    def _save_local(self) -> None:
        """Save local.json and update line count."""
        content = json.dumps(self._local, indent=2, ensure_ascii=False)
        self._local["metadata"]["current_lines"] = content.count("\n") + 1
        self._save(self._local_path, self._local)

    def _save_observations(self) -> None:
        """Save observations.json and update line count."""
        content = json.dumps(self._observations, indent=2, ensure_ascii=False)
        self._observations["metadata"]["current_lines"] = content.count("\n") + 1
        self._save(self._observations_path, self._observations)

    def _now(self) -> str:
        """Return current UTC time as ISO string."""
        return datetime.now(timezone.utc).isoformat()

    def _next_session_number(self) -> int:
        """Return the next session number."""
        sessions = self._local.get("sessions", [])
        if not sessions:
            return 1
        return max(s.get("session_number", 0) for s in sessions) + 1

    def start_session(self) -> int:
        """Start a new session. Returns the session number."""
        session_num = self._next_session_number()
        self._current_session = {
            "session_number": session_num,
            "date": self._now(),
            "activities": [],
            "status": "in_progress",
        }
        self._session_active = True
        self._local["sessions"].append(self._current_session)
        self._save_local()
        return session_num

    def log_activity(self, activity: str) -> None:
        """Log an activity to the current session."""
        if not self._session_active or self._current_session is None:
            raise RuntimeError("No active session. Call start_session() first.")
        self._current_session["activities"].append(activity)
        self._save_local()

    def add_learning(self, key: str, value: str) -> None:
        """Add a key learning with timestamp."""
        if "key_learnings" not in self._local:
            self._local["key_learnings"] = {}
        self._local["key_learnings"][key] = f"{value} [{self._now()}]"
        self._save_local()

    def end_session(self) -> None:
        """End the current session."""
        if not self._session_active or self._current_session is None:
            raise RuntimeError("No active session to end.")
        self._current_session["status"] = "completed"
        self._session_active = False

        # Update recently_completed
        completed = self._local["active"].get("recently_completed", [])
        for activity in self._current_session["activities"]:
            completed.append(activity)
        self._local["active"]["recently_completed"] = completed[-20:]

        self._current_session = None
        self._save_local()

    def observe(self, observation: str, tags: Optional[list] = None) -> None:
        """Record a collaboration observation."""
        if tags is None:
            tags = []

        session_num = 0
        if self._current_session:
            session_num = self._current_session["session_number"]
        elif self._local["sessions"]:
            session_num = self._local["sessions"][-1]["session_number"]

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        today_block = None
        for obs in self._observations["observations"]:
            obs_date = obs.get("date", "")
            if obs_date.startswith(today):
                today_block = obs
                break

        entry = {
            "title": observation[:60],
            "observation": observation,
            "tags": tags,
        }

        if today_block:
            today_block["entries"].append(entry)
            today_block["session"] = session_num
        else:
            self._observations["observations"].append(
                {
                    "date": self._now(),
                    "session": session_num,
                    "entries": [entry],
                }
            )

        self._save_observations()

    def get_context(self) -> str:
        """Return a formatted string for system prompt injection.

        Combines identity, current focus, recent sessions, key learnings,
        and recent observations into a readable context block.
        """
        lines = []
        lines.append("# Agent Context (Trinity Pattern)")
        lines.append("")

        # Identity
        identity = self._id.get("identity", {})
        lines.append(f"## Identity: {identity.get('name', 'Unknown')}")
        lines.append(f"**Role:** {identity.get('role', 'Unknown')}")
        if identity.get("traits"):
            lines.append(f"**Traits:** {identity['traits']}")
        if identity.get("purpose"):
            lines.append(f"**Purpose:** {identity['purpose']}")
        if identity.get("principles"):
            lines.append("**Principles:** " + " | ".join(identity["principles"]))
        lines.append("")

        # Current focus
        active = self._local.get("active", {})
        if active.get("current_focus"):
            lines.append(f"## Current Focus\n{active['current_focus']}")
            lines.append("")

        # Recent sessions (last 5)
        sessions = self._local.get("sessions", [])
        if sessions:
            recent = sessions[-5:]
            lines.append("## Recent Sessions")
            for s in reversed(recent):
                status = s.get("status", "unknown")
                date = s.get("date", "")[:10]
                activities = s.get("activities", [])
                lines.append(
                    f"- Session {s.get('session_number')}"
                    f" ({date}, {status}): " + "; ".join(activities[:5])
                )
            lines.append("")

        # Key learnings
        learnings = self._local.get("key_learnings", {})
        if learnings:
            lines.append("## Key Learnings")
            for key, val in list(learnings.items())[-10:]:
                lines.append(f"- **{key}:** {val}")
            lines.append("")

        # Recent observations (last 3 blocks)
        obs_list = self._observations.get("observations", [])
        if obs_list:
            recent_obs = obs_list[-3:]
            lines.append("## Recent Observations")
            for block in reversed(recent_obs):
                for entry in block.get("entries", [])[:3]:
                    tags = ", ".join(entry.get("tags", []))
                    tag_str = f" [{tags}]" if tags else ""
                    lines.append(f"- {entry.get('observation', '')}{tag_str}")
            lines.append("")

        return "\n".join(lines)

    def needs_rollover(self) -> bool:
        """Check if local.json exceeds the configured max_lines."""
        max_lines = self._local.get("config", {}).get("max_lines", 600)
        current = self._local.get("metadata", {}).get("current_lines", 0)
        return current >= max_lines

    def rollover(self) -> list:
        """Extract oldest sessions via FIFO. Returns extracted sessions.

        Removes the oldest half of sessions when rollover is triggered.
        Returns the extracted sessions for external archival.
        """
        sessions = self._local.get("sessions", [])
        if not sessions:
            return []

        lines_before = self._local["metadata"].get("current_lines", 0)

        # Extract oldest half
        split = len(sessions) // 2
        if split < 1:
            split = 1
        extracted = sessions[:split]
        self._local["sessions"] = sessions[split:]

        # Record rollover
        self._local["metadata"]["rollover_history"].append(
            {
                "date": self._now(),
                "sessions_extracted": len(extracted),
                "lines_before": lines_before,
            }
        )

        self._save_local()

        # Update lines_after in the history entry
        self._local["metadata"]["rollover_history"][-1]["lines_after"] = self._local["metadata"][
            "current_lines"
        ]
        self._save_local()

        return extracted
