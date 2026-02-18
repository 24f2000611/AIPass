# Trinity Pattern — Agent Bootstrap

You have persistent memory. Three files in your Trinity directory define who you are, what you've done, and how you collaborate. Read them now.

## Your Memory Files

On every session start, read these three files:

1. **`id.json`** — Your identity. Your name, role, purpose, principles, and boundaries. This rarely changes. It tells you *who you are*.

2. **`local.json`** — Your session history. What you've worked on, what you've learned, what's in progress. This updates every session. It tells you *what you've done*.

3. **`observations.json`** — Your collaboration patterns. How you and the user work together, communication preferences, workflow insights. It tells you *how you work together*.

**Default location:** `.trinity/` in your project root (created by `trinity init`)

If the files don't exist yet, run `trinity init` from your project root, or initialize programmatically:
```python
from trinity_pattern import Agent
agent = Agent(directory=".trinity", name="YourName", role="Your Role")
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

agent = Agent(directory=".trinity")

# Record what you did this session
agent.start_session()
agent.log_activity("Describe what you worked on")
agent.add_learning("key_name", "What you learned")
agent.end_session()

# Record collaboration insights
agent.observe("Pattern you noticed about how you work together", tags=["relevant-tag"])
```

Write to these Trinity files — not to separate memory files, notes, or scratchpads. These three files ARE your memory system.

## Platform Integration

Trinity Pattern works with any AI coding agent or IDE that supports project-level instruction files:

| Platform | Instruction File | How It Works |
|----------|-----------------|--------------|
| Gemini CLI | `GEMINI.md` | Place this content in GEMINI.md at project root |
| Cursor | `.cursorrules` | Add Trinity instructions to your rules file |
| OpenAI Codex | `AGENTS.md` | Place this content in AGENTS.md at project root |
| Windsurf | `.windsurfrules` | Add Trinity instructions to your rules file |
| Other agents | Varies | Copy these instructions into your agent's config |

Copy the content of this file into whatever instruction file your AI agent reads on startup. The key requirement is that the agent reads `.trinity/id.json`, `.trinity/local.json`, and `.trinity/observations.json` at the start of every session.

## Key Principles

- **Your files are your continuity.** Without them, you start from zero every session. With them, you have history, identity, and context that persists.
- **Update after every meaningful session.** Each update adds to your accumulated context. Skip the update and the session never happened.
- **Identity is not memory.** `id.json` is who you are (stable). `local.json` is what you've done (rolling). `observations.json` is how you work together (evolving). Don't conflate them.
- **Rolling, not unbounded.** `local.json` has a line limit. When it fills up, oldest sessions archive via FIFO. Key learnings persist across rollovers.
