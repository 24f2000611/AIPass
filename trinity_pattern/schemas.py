"""Default schema templates for Trinity Pattern files."""

TRINITY_VERSION = "1.0.0"


def default_id(name: str, role: str, platform: str = "generic") -> dict:
    """Return a default id.json structure."""
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).isoformat()
    return {
        "trinity_version": TRINITY_VERSION,
        "identity": {
            "name": name,
            "role": role,
            "traits": "",
            "purpose": "",
            "what_i_do": [],
            "what_i_dont_do": [],
            "principles": [],
        },
        "metadata": {
            "created": now,
            "last_updated": now,
            "platform": platform,
        },
    }


def default_local() -> dict:
    """Return a default local.json structure."""
    return {
        "trinity_version": TRINITY_VERSION,
        "config": {
            "max_lines": 600,
            "max_sessions": 50,
            "rollover_strategy": "fifo",
        },
        "active": {
            "current_focus": "",
            "recently_completed": [],
        },
        "sessions": [],
        "key_learnings": {},
        "metadata": {
            "current_lines": 0,
            "rollover_history": [],
        },
    }


def default_observations() -> dict:
    """Return a default observations.json structure."""
    return {
        "trinity_version": TRINITY_VERSION,
        "config": {
            "max_lines": 600,
            "content_focus": "relationship and collaboration, not technical progress",
        },
        "observations": [],
        "metadata": {
            "current_lines": 0,
            "rollover_history": [],
        },
    }
