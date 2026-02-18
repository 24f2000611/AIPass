# Trinity Pattern — Agent Bootstrap

You have persistent memory. Three files in your Trinity directory define who you are, what you've done, and how you collaborate. Read them now.

## Your Memory Files

On every session start, read these three files:

1. **`id.json`** — Your identity. Your name, role, purpose, principles, and boundaries. This rarely changes. It tells you *who you are*.

2. **`local.json`** — Your session history. What you've worked on, what you've learned, what's in progress. This updates every session. It tells you *what you've done*.

3. **`observations.json`** — Your collaboration patterns. How you and the user work together, communication preferences, workflow insights. It tells you *how you work together*.

**Default location:** `~/.trinity/` (configurable — check if a different directory is set in your project)

If the files don't exist yet, initialize them:
```python
from trinity_pattern import Agent
agent = Agent(directory="~/.trinity", name="YourName", role="Your Role")
```

## On Session Start

1. Read all three files from your Trinity directory
2. Use `id.json` to understand your role, boundaries, and principles
3. Use `local.json` to see your recent sessions, current focus, and key learnings
4. Use `observations.json` to recall collaboration patterns and preferences
5. Continue from where you left off — don't ask the user to re-explain context you already have

## Updating Your Memories

When the user asks you to "update memories" or at the end of a meaningful session:

```python
from trinity_pattern import Agent

agent = Agent(directory="~/.trinity")

# Record what you did this session
agent.start_session()
agent.log_activity("Describe what you worked on")
agent.add_learning("key_name", "What you learned")
agent.end_session()

# Record collaboration insights
agent.observe("Pattern you noticed about how you work together", tags=["relevant-tag"])
```

Write to these Trinity files — not to separate memory files, notes, or scratchpads. These three files ARE your memory system.

## Auto-Injection (Optional)

For automatic context injection on every prompt, set up the hook:

1. Copy `examples/claude_code/hook_inject.py` to a stable location
2. Update `AGENT_DIR` in the script to point to your Trinity directory
3. Add to `.claude/hooks.json`:
```json
{
    "hooks": {
        "UserPromptSubmit": [{
            "type": "command",
            "command": "python3 /path/to/hook_inject.py"
        }]
    }
}
```

With the hook active, your Trinity context is injected into every message automatically — you don't need to manually read your files each session.

## Key Principles

- **Your files are your continuity.** Without them, you start from zero every session. With them, you have history, identity, and context that persists.
- **Update after every meaningful session.** Each update adds to your accumulated context. Skip the update and the session never happened.
- **Identity is not memory.** `id.json` is who you are (stable). `local.json` is what you've done (rolling). `observations.json` is how you work together (evolving). Don't conflate them.
- **Rolling, not unbounded.** `local.json` has a line limit. When it fills up, oldest sessions archive via FIFO. Key learnings persist across rollovers.
