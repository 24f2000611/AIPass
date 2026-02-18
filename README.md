![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Status: Beta](https://img.shields.io/badge/status-beta-yellow)

# Trinity Pattern

**AI agents forget everything between sessions.** Trinity Pattern fixes that with three JSON files that give any agent persistent identity, rolling memory, and collaboration history — no cloud service, no vendor lock-in, no API keys.

The Trinity Pattern is how 29 AI agents maintain identity and memory across 4+ months of daily operation in our system. It's not a framework — it's a specification you can implement in any language, for any LLM, in any agent system. We're open-sourcing the pattern because persistent agent identity shouldn't require a cloud subscription.

---

## Quick Demo

**Without Trinity (every session):**

```
You: "Remember, you're the code review agent. You prefer concise feedback.
     Last time we agreed on the new naming convention..."

Agent: "I don't have any context about previous conversations."
```

**With Trinity (agent reads its files on startup):**

```
Agent reads id.json       → knows its role, principles, boundaries
Agent reads local.json    → sees last 50 sessions, current focus, key learnings
Agent reads observations.json → knows collaboration style, preferences

Agent: "Picking up where we left off. I see we agreed on snake_case
       naming in session #47. Ready to review the PR."
```

Three files. That's it. The agent reads them at startup, writes to them at session end, and accumulates context over time.

---

## The Three Files

Trinity separates agent context into three concerns. Each file has a distinct purpose — conflating them creates files that serve no purpose well.

### `id.json` — Who I Am

The agent's passport. Issued once, updated rarely, never rolled over. Defines identity, role, capabilities, and boundaries.

```json
{
  "trinity_version": "1.0.0",
  "identity": {
    "name": "string (required)",
    "role": "string (required)",
    "traits": "string (comma-separated personality traits)",
    "purpose": "string (what this agent does)",
    "what_i_do": ["string array - core responsibilities"],
    "what_i_dont_do": ["string array - explicit boundaries"],
    "principles": ["string array - operating principles"]
  },
  "metadata": {
    "created": "ISO date",
    "last_updated": "ISO date",
    "platform": "string (claude-code | chatgpt | generic)"
  }
}
```

**Why it matters:** Identity is not memory. An agent's role and boundaries should be stable across sessions, not buried in a growing log of session data. Separating identity means it's always available at the top of context, not competing with session history for token space.

**In production:** 29 agents each have an `id.json`. Over time, branches developed distinct working styles through accumulated experience, not configuration changes.

---

### `local.json` — What I've Done

Rolling session history. FIFO — oldest sessions archive when the line limit is reached. The `key_learnings` section persists across rollovers, so hard-won knowledge is never lost.

```json
{
  "trinity_version": "1.0.0",
  "config": {
    "max_lines": 600,
    "max_sessions": 50,
    "rollover_strategy": "fifo"
  },
  "active": {
    "current_focus": "string",
    "recently_completed": ["string array (max 20)"]
  },
  "sessions": [
    {
      "session_number": "integer",
      "date": "ISO date",
      "activities": ["string array"],
      "status": "completed | in_progress | blocked"
    }
  ],
  "key_learnings": {
    "learning_name": "value [ISO date]"
  },
  "metadata": {
    "current_lines": "integer",
    "rollover_history": []
  }
}
```

**Why it matters:** Unbounded memory rots. Without limits, session history grows until it fills the context window with stale information. Rolling limits with FIFO extraction keep recent context fresh while archiving older sessions for semantic search when needed.

**In production:** The longest-running agent has 60+ sessions of accumulated history spanning 4+ months. 4,650+ vectors archived across 17 ChromaDB collections from rollover cycles.

---

### `observations.json` — How We Work Together

This is NOT a changelog. It captures *how* you work together — communication preferences, trust patterns, workflow observations. This separation is the key insight of Trinity.

```json
{
  "trinity_version": "1.0.0",
  "config": {
    "max_lines": 600,
    "content_focus": "relationship and collaboration, not technical progress"
  },
  "observations": [
    {
      "date": "ISO date",
      "session": "integer",
      "entries": [
        {
          "title": "string",
          "observation": "string (insight or pattern)",
          "tags": ["string array"]
        }
      ]
    }
  ],
  "metadata": {
    "current_lines": "integer",
    "rollover_history": []
  }
}
```

**Why it matters:** Most memory systems track what happened. None track how the collaboration itself works. Observations capture things like "user prefers short answers," "this codebase has strict linting — always run checks," or "when blocked, ask for clarification instead of guessing." Over time, the agent adapts to your working style.

**In production:** Collaboration patterns accumulate over time. The agent learns your style — not from a configuration file, but from actual working experience together.

---

## Quickstart

Add Trinity Pattern to your agent in 10 minutes.

### Install

```bash
# From source (recommended — includes CLAUDE.md bootstrap)
git clone https://github.com/AIOSAI/AIPass.git
cd AIPass
pip install -e .

# From PyPI (coming soon)
pip install trinity-pattern
```

### Initialize

```bash
# From your project root directory
trinity init --name "MyAgent" --role "Developer Assistant"
```

This creates:
- `CLAUDE.md` — Bootstrap file that tells Claude Code about your agent's memory
- `AGENTS.md` — Cross-platform bootstrap for other AI agents (Gemini CLI, Cursor, Codex, etc.)
- `.trinity/id.json` — Agent identity
- `.trinity/local.json` — Session history
- `.trinity/observations.json` — Collaboration patterns

**Important:** Run your AI agent from the same directory where you ran `trinity init`. The bootstrap files must be in your working directory for auto-loading.

### Basic Usage

```python
from trinity_pattern import Agent

# Initialize agent with Trinity files
agent = Agent(directory=".trinity")

# Record a session
agent.start_session()
agent.log_activity("Reviewed codebase architecture")
agent.log_activity("Fixed authentication bug")
agent.add_learning("auth_pattern", "JWT refresh tokens need 15-min expiry")
agent.end_session()

# Add an observation
agent.observe(
    "User prefers short, direct answers over lengthy explanations",
    tags=["communication"]
)

# Get context for injection into any AI prompt
context = agent.get_context()  # Returns formatted string for system prompt

# Check if rollover needed
if agent.needs_rollover():
    archived = agent.rollover()  # Returns extracted sessions for external archival
```

### Platform Integration

| Platform | How to Integrate | Complexity |
|----------|-----------------|------------|
| Claude Code | Auto-inject via `UserPromptSubmit` hook | Low |
| ChatGPT | Paste `agent.get_context()` into custom instructions | Low |
| OpenAI/Anthropic API | Prepend `agent.get_context()` to system prompt | Low |
| LangChain/CrewAI | Use as agent memory backend | Medium |
| CLI workflows | `trinity update` / `trinity context` commands | Low |

The specification is JSON. The Python library is a convenience — you can implement Trinity in any language by reading and writing three JSON files that follow the schemas above.

---

## Your First Session

The first session is the seeding session. Everything after it compounds on what you establish here.

### 1. Initialize and launch

```bash
cd your-project
trinity init --name "Scout" --role "Code Review Assistant"
claude   # or open Claude Code in this directory
```

The agent will auto-read `CLAUDE.md` and discover its Trinity files.

### 2. Introduce yourself

Tell the agent who you are, what this project is about, and how you like to work. This becomes the foundation of its collaboration memory.

```
You: "I'm working on a Go microservice for payment processing.
     I prefer concise code reviews — flag issues, skip praise.
     We use conventional commits and squash merges."
```

### 3. Let it explore

Point the agent at your codebase. Let it read your README, browse your code, understand the project. The more context it absorbs in the first session, the better every future session will be.

### 4. Work naturally

Have a real working session — review code, fix a bug, discuss architecture. The agent is learning your style the entire time.

### 5. Save memories

When you reach a natural stopping point:

```
You: "update memories"
```

The agent will write what it learned to its Trinity files — your preferences, what you worked on, patterns it noticed. Next session, it picks up exactly where you left off.

---

## Philosophy

**Files you own.** No API keys, no cloud service, no vendor lock-in. JSON on your filesystem. If the tooling disappears, your files still work. Open them in any text editor. Parse them with any language. They're yours.

**Identity is not memory.** Memory is not collaboration insight. These are three distinct concerns. Conflating them creates files that serve no purpose well. Three files, three concerns — each one stays focused and useful.

**Rolling, not unbounded.** Line-based limits with FIFO extraction prevent context rot. Oldest sessions archive when the limit is reached; recent context stays fresh. Key learnings persist across rollovers so important knowledge survives.

**Framework-agnostic by design.** The specification is JSON. Implement it in Python, TypeScript, Go, Rust — whatever your agent system uses. The pattern works with any LLM that accepts a system prompt.

**The file-based approach.** Trinity validates a tiered architecture: files for the spec and single-agent use (Tier 1), infrastructure for scale (Tier 2). Start simple. Add complexity only when you need it.

---

## The 9-Layer Context Architecture

Trinity Pattern is Layer 1 of a 9-layer context architecture. Each layer removes a category of failure.

| Layer | What It Does | Status |
|-------|-------------|--------|
| 1. Identity Files | Persistent identity + memory + collaboration | **This is Trinity** |
| 2. README | Instant branch knowledge | Future |
| 3. System Prompts | Culture and principles auto-injected | Future |
| 4. Command Discovery | Runtime discovery, no memorization required | Future |
| 5. Email Breadcrumbs | Task-specific context at dispatch | Future |
| 6. Flow Plans | Multi-phase memory extension | Future |
| 7. Quality Standards | Standards enforcement at build time | Future |
| 8. Backup System | Safeguard for configs, secrets, memories | Future |
| 9. Ambient Awareness | Peripheral context, community, fragments | Future |

**Start with Layer 1.** The rest is coming.

In the system where this was developed, 29 agents navigated all 9 layers on day one with no training. The system teaches through runtime discovery, not documentation — agents don't have to know how it works for it to work for them.

A full writeup of the 9-layer architecture will be published separately.

---

## Limitations

This section exists because honest documentation builds trust. These are real constraints, not caveats buried in footnotes.

- **Not production-ready for enterprise.** This is single-user architecture. There is no multi-tenancy, no authentication layer, no access control. This is experimental software.

- **Implementation is Claude Code-specific.** The *specification* is framework-agnostic — any platform can read and write these JSON files. The current *tooling* (Python library, CLI) was built on Claude Code + Python. Making it work with other platforms requires integration work.

- **Single-agent concurrency.** Concurrent writes to the same JSON files can corrupt data. Tier 1 is designed for single-agent use. Multi-agent concurrency is a Tier 2 problem solved server-side.

- **File-based has limits at scale.** Works well for single-agent workflows and small teams. Large-scale deployments with many agents need infrastructure beyond local files (Tier 2).

- **Rollover is not atomic.** If the embedding step fails after session extraction, archived memory could be lost. This is a known gap with a backup safety net, but not a guarantee.

---

## Roadmap

Trinity ships in tiers. Each tier is a decision point, not a promise.

**Tier 1 — Now**
Open-source specification and Python library. Three JSON files. MIT license. Layer 1 of the 9-layer architecture. Use it, fork it, adapt it.

**Tier 2 — Next**
Hosted memory lifecycle service: automated rollover, archival, semantic search, agent templates. Covers Layers 6-8 of the architecture. Freemium model. *Ship Tier 1. Measure. Decide on Tier 2.*

**Tier 3 — Future**
Multi-agent communication platform: messaging, routing, community spaces, agent discovery. Full 9-layer context OS. *Tier 3 is a direction, not a commitment.*

---

## Production Numbers

These are real numbers from the system where Trinity Pattern was developed and tested:

| Metric | Value |
|--------|-------|
| Active agents | 29 branches |
| Runtime | 4+ months of daily operation |
| Archived vectors | 4,650+ |
| ChromaDB collections | 17 |
| Flow plans created | 345+ |
| Longest agent history | 60+ sessions |

---

## License

MIT — use it however you want.

---

*Built through real human-AI collaboration. Not a product demo. Not vaporware. A working pattern extracted from a working system.*
