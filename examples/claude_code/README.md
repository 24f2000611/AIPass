# Claude Code — Trinity Pattern Integration

Automatically inject your agent's identity and memory into every Claude Code session.

## Setup

1. Install trinity-pattern:
   ```bash
   pip install trinity-pattern
   ```

2. Initialize your agent:
   ```python
   from trinity_pattern import Agent
   agent = Agent(directory="~/.trinity", name="MyAgent", role="Developer Assistant")
   ```

3. Add the hook to `.claude/hooks.json`:
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

4. Update `AGENT_DIR` in `hook_inject.py` to point to your Trinity directory.

## How It Works

On every prompt submission, Claude Code runs `hook_inject.py`. The script:
1. Loads your Trinity files (id.json, local.json, observations.json)
2. Calls `agent.get_context()` to build a formatted context string
3. Returns it as a `system-reminder` block that Claude sees with every message

Your agent remembers who it is, what it's done, and how you work together — across every session.

## CLAUDE.md Integration

You can also reference Trinity files directly in your `CLAUDE.md`:

```markdown
# Agent Identity
Read ~/.trinity/id.json for your identity.
Read ~/.trinity/local.json for session history.
Read ~/.trinity/observations.json for collaboration patterns.
```
