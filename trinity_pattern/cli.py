"""CLI entry point for Trinity Pattern.

Usage:
    trinity init [--name NAME] [--role ROLE] [--dir DIR]
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

from .schemas import TRINITY_VERSION, default_id, default_local, default_observations


def _get_template_path():
    """Get the path to the bundled CLAUDE.md template."""
    return Path(__file__).parent / "templates" / "CLAUDE.md"


def cmd_init(args):
    """Initialize Trinity Pattern in the current directory."""
    target_dir = Path(args.dir)
    trinity_dir = target_dir / ".trinity"
    claude_md = target_dir / "CLAUDE.md"

    created = []
    skipped = []

    # Create .trinity directory
    trinity_dir.mkdir(parents=True, exist_ok=True)

    # Create Trinity files (don't overwrite existing)
    files = {
        "id.json": default_id(args.name, args.role, "claude-code"),
        "local.json": default_local(),
        "observations.json": default_observations(),
    }

    for filename, data in files.items():
        path = trinity_dir / filename
        if path.exists():
            skipped.append(f".trinity/{filename}")
        else:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")
            created.append(f".trinity/{filename}")

    # Copy CLAUDE.md template (don't overwrite existing)
    if claude_md.exists():
        skipped.append("CLAUDE.md")
    else:
        template = _get_template_path()
        if template.exists():
            shutil.copy2(template, claude_md)
            created.append("CLAUDE.md")
        else:
            # Fallback: template not found in package
            print(f"Warning: CLAUDE.md template not found at {template}", file=sys.stderr)

    # Report results
    if created:
        print(f"Initialized Trinity Pattern (v{TRINITY_VERSION})")
        print(f"  Agent: {args.name} ({args.role})")
        print(f"  Directory: {trinity_dir}")
        print()
        for f in created:
            print(f"  Created: {f}")
    if skipped:
        print()
        for f in skipped:
            print(f"  Skipped (already exists): {f}")

    if created:
        print()
        print("Next steps:")
        print("  1. Open Claude Code from this directory")
        print("  2. Say 'hi' — your agent will read CLAUDE.md and discover its memory files")
        print("  3. Have a conversation — introduce yourself, share your project context")
        print("  4. Say 'update memories' — the agent will save what it learned")
    elif not skipped:
        print("Nothing to do — Trinity Pattern is already initialized.")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="trinity",
        description="Trinity Pattern — Persistent identity for AI agents",
    )
    subparsers = parser.add_subparsers(dest="command")

    # init command
    init_parser = subparsers.add_parser(
        "init", help="Initialize Trinity Pattern in current directory"
    )
    init_parser.add_argument("--name", default="Agent", help="Agent name (default: Agent)")
    init_parser.add_argument(
        "--role", default="AI Assistant", help="Agent role (default: AI Assistant)"
    )
    init_parser.add_argument("--dir", default=".", help="Target directory (default: current)")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
