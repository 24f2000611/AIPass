# Contributing to Trinity Pattern

Thanks for your interest in contributing. Trinity Pattern is experimental software built through real human-AI collaboration. We welcome contributions that make the pattern more useful, more correct, or more accessible.

---

## What This Project Is

Trinity Pattern is Layer 1 of a 9-layer context architecture — three JSON files that give AI agents persistent identity, rolling memory, and collaboration history. It's not a framework. It's a specification and a Python library.

This is an experimental project. It works reliably in production for one system (29 agents, 4+ months), but it's not enterprise software. Contributions should match that reality — practical improvements over architectural astronautics.

---

## How to Contribute

### 1. Fork and Branch

```bash
git clone https://github.com/AIOSAI/AIPass.git
cd AIPass
git checkout -b your-feature-name
```

Use descriptive branch names: `fix-rollover-edge-case`, `add-typescript-example`, `docs-clarify-observations`.

### 2. Make Your Changes

- Follow existing code style and patterns
- Keep changes focused — one concern per PR
- If you're changing the specification (JSON schemas), explain why in your PR description

### 3. Test

- Run existing tests before submitting
- Add tests for new functionality
- If your change affects the three JSON file schemas, verify backwards compatibility

### 4. Submit a Pull Request

- Write a descriptive title (not "fix stuff" or "updates")
- Explain **what** changed and **why**
- Reference any related issues
- Keep PRs reasonably scoped — large PRs are harder to review

---

## PR Guidelines

- **Descriptive titles**: "Fix FIFO rollover when sessions span midnight" not "bug fix"
- **Explain the why**: The PR description should explain motivation, not just list files changed
- **Tests matter**: If you're changing behavior, show that it works
- **Docs follow code**: If you change how something works, update the relevant documentation
- **One concern per PR**: Don't bundle unrelated changes

---

## What We're Looking For

Contributions we'd especially value:

- **Bug fixes** in the Python library or CLI
- **Alternative implementations** (TypeScript, Go, Rust — the spec is JSON, implement it anywhere)
- **Documentation improvements** — clearer explanations, better examples, typo fixes
- **Edge case handling** in rollover, memory limits, or file operations
- **Real-world usage reports** — how you used Trinity, what worked, what didn't

---

## Code of Conduct

Be respectful. Be constructive. Assume good intent.

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). In short: be welcoming, be patient, be thoughtful. We're building something together.

---

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE). This project is and will remain open source.

---

## Questions?

Open an issue. We'd rather answer a question than have you struggle in silence.

---

*Trinity Pattern is experimental software that works. Contributions that keep it honest, useful, and accessible are always welcome.*
