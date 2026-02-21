# Roadmap

Where Trinity Pattern is today, where it's headed, and how you can help.

Last updated: February 2026

---

## What Exists Today

These are shipped and working. You can use them right now.

- [x] **Trinity Pattern specification v1.0.0** -- three JSON files (`id.json`, `local.json`, `observations.json`) with documented schemas
- [x] **JSON Schema files** -- formal JSON Schema (draft-07) for all three file types, usable for validation in any language
- [x] **Python library** -- `Agent` class with session management, activity logging, key learnings, observations, context generation, and FIFO rollover
- [x] **CLI tool** -- `trinity init` creates `.trinity/` directory, all three JSON files, `CLAUDE.md` bootstrap, and `AGENTS.md` cross-platform bootstrap in one command
- [x] **Claude Code integration** -- hook script (`hook_inject.py`) that auto-injects Trinity context on every prompt via `UserPromptSubmit`
- [x] **ChatGPT integration** -- context generator script that outputs formatted context for custom instructions
- [x] **Generic LLM integration** -- API prepend example with OpenAI, Anthropic, and raw HTTP examples
- [x] **Cross-platform bootstrap** -- `AGENTS.md` template for Gemini CLI, Cursor, Codex, and other AI agents
- [x] **Test suite** -- 25+ unit tests covering init, sessions, learnings, observations, context generation, rollover, and persistence
- [x] **CI pipeline** -- GitHub Actions with ruff linting, pytest across Python 3.8-3.13 on Ubuntu/macOS/Windows, coverage reporting
- [x] **Packaging** -- `pyproject.toml` and `setup.py` ready for PyPI distribution, built wheel and sdist in `dist/`
- [x] **Docker support** -- Dockerfile and docker-compose.yml for reproducible multi-version testing
- [x] **Security tooling** -- dependabot config, pip-audit, safety checks, CodeQL scanning via GitHub Actions
- [x] **Issue templates** -- bug report and feature request templates, auto-triage workflow, stale issue management
- [x] **CONTRIBUTING.md** -- contributor guide with fork/branch/test/PR workflow
- [x] **MIT license**

**What's proven in production:** 32 agents running this pattern daily for 4+ months. 60+ sessions on the longest-running agent. 5,500+ archived vectors across 21 ChromaDB collections from rollover cycles.

---

## Coming Soon

Actively planned or in progress. No dates promised -- these ship when they're ready.

- [ ] **PyPI package publication** -- `pip install trinity-pattern` working from the public registry (package is built, awaiting PyPI account setup)
- [ ] **`trinity update` CLI command** -- update session history and observations from the command line without writing Python
- [ ] **`trinity context` CLI command** -- output current agent context to stdout for piping into other tools
- [ ] **`trinity status` CLI command** -- show current agent state: session count, line usage, rollover status
- [ ] **Observations rollover** -- FIFO rollover for `observations.json` matching the existing `local.json` rollover behavior
- [ ] **Integration tests for examples** -- automated CI validation that all example scripts (Claude Code, ChatGPT, generic LLM) produce expected output
- [ ] **API documentation** -- auto-generated docs from docstrings, published to GitHub Pages
- [ ] **Coverage badge** -- Codecov integration with coverage badge in README
- [ ] **More examples** -- multi-session workflow, team of agents sharing observations, CI/CD agent that persists across pipeline runs
- [ ] **Validation helper** -- `Agent.validate()` method that checks Trinity files against the JSON schemas

---

## On the Horizon

Aspirational. These represent directions we're interested in, not commitments. Community interest and contributions will shape what actually gets built.

- [ ] **TypeScript implementation** -- a `trinity-pattern` npm package implementing the same spec
- [ ] **Go implementation** -- for teams building agents in Go
- [ ] **Rust implementation** -- for performance-sensitive or embedded agent systems
- [ ] **LangChain memory backend** -- use Trinity files as the memory layer for LangChain agents
- [ ] **CrewAI integration** -- Trinity-based agent identity for CrewAI multi-agent workflows
- [ ] **Tier 2: Hosted memory lifecycle** -- automated rollover, archival to vector store, semantic search over archived sessions (this would be a separate service, not part of the open-source library)
- [ ] **Agent templates** -- pre-built identity configurations for common agent roles (code reviewer, documentation writer, DevOps assistant)
- [ ] **Standards participation** -- engaging with NIST and AAIF on agent identity standards, contributing Trinity's approach to the conversation
- [ ] **Multi-agent coordination** -- patterns for multiple agents sharing context without file conflicts
- [ ] **9-layer architecture writeup** -- full public documentation of the 9-layer context architecture that Trinity is Layer 1 of

---

## How to Contribute

We're a small team and contributions genuinely help. Here's where to start:

**Low-hanging fruit:**
- Try `trinity init` in your project and tell us what broke (file an issue)
- Improve documentation -- clearer explanations, better examples, typo fixes
- Add edge case tests for rollover, file operations, or concurrent access

**Medium effort:**
- Build an example integration for your favorite AI platform
- Implement the spec in another language (the JSON schemas are the source of truth)
- Add CLI commands (`trinity update`, `trinity context`, `trinity status`)

**Big swings:**
- Build a LangChain or CrewAI memory backend using Trinity files
- Create a VS Code extension that shows Trinity agent status
- Write a tutorial or blog post about using Trinity in your workflow

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide. Open an issue if you have questions -- we'd rather help than have you stuck.

---

*This roadmap is a living document. Items move, get cut, or get added based on what we learn. If something here matters to you, open an issue or start a discussion -- community signal drives priority.*
