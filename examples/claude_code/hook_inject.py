#!/usr/bin/env python3
"""Claude Code hook script for Trinity Pattern context injection.

Usage:
    Add to your Claude Code hooks configuration (.claude/hooks.json):

    {
        "hooks": {
            "UserPromptSubmit": [{
                "type": "command",
                "command": "python3 /path/to/hook_inject.py"
            }]
        }
    }

    The hook runs on every prompt submission and injects the agent's
    Trinity context into the system prompt via stdout.
"""

import json
import sys
from pathlib import Path

from trinity_pattern import Agent

# Configure: point to your agent's Trinity directory
AGENT_DIR = Path.home() / ".trinity"


def main():
    """Inject Trinity context into Claude Code system prompt."""
    # Read the hook input from stdin (required by Claude Code hook protocol)
    _hook_input = json.loads(sys.stdin.read())

    agent = Agent(directory=str(AGENT_DIR))
    context = agent.get_context()

    # Output as system-reminder for Claude Code injection
    result = {"output": f"<system-reminder>\n{context}\n</system-reminder>"}
    json.dump(result, sys.stdout)


if __name__ == "__main__":
    main()
