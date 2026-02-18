#!/usr/bin/env python3
"""Generate Trinity context for ChatGPT custom instructions.

Usage:
    python3 generate_context.py [--dir PATH]

    Outputs a formatted context string. Copy the output and paste it
    into ChatGPT's custom instructions (Settings > Personalization).
"""

import argparse
from pathlib import Path

from trinity_pattern import Agent


def main():
    parser = argparse.ArgumentParser(
        description="Generate Trinity context for ChatGPT custom instructions"
    )
    parser.add_argument(
        "--dir",
        default=str(Path.home() / ".trinity"),
        help="Path to Trinity agent directory (default: ~/.trinity)",
    )
    parser.add_argument(
        "--name",
        default="Assistant",
        help="Agent name for first-time setup (default: Assistant)",
    )
    parser.add_argument(
        "--role",
        default="AI Assistant",
        help="Agent role for first-time setup (default: AI Assistant)",
    )
    args = parser.parse_args()

    agent = Agent(
        directory=args.dir,
        name=args.name,
        role=args.role,
        platform="chatgpt",
    )

    context = agent.get_context()

    print("=" * 60)
    print("COPY EVERYTHING BELOW INTO CHATGPT CUSTOM INSTRUCTIONS")
    print("=" * 60)
    print()
    print(context)
    print()
    print("=" * 60)
    print("END — Paste the above into Settings > Personalization")
    print("=" * 60)


if __name__ == "__main__":
    main()
