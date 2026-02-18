#!/usr/bin/env python3
"""Generic LLM API integration with Trinity Pattern context.

Shows how to prepend Trinity context to any LLM API call.
Works with OpenAI, Anthropic, or any chat completion API.

Usage:
    python3 api_prepend.py

    Set your API key via environment variable before running:
    export OPENAI_API_KEY=sk-...
    # or
    export ANTHROPIC_API_KEY=sk-ant-...
"""

from pathlib import Path

from trinity_pattern import Agent

# Initialize agent
agent = Agent(
    directory=str(Path.home() / ".trinity"),
    name="APIBot",
    role="General Assistant",
    platform="generic",
)

# Get Trinity context
context = agent.get_context()

# Your base system prompt
BASE_PROMPT = "You are a helpful assistant."

# Combined prompt with Trinity context prepended
system_prompt = context + "\n---\n" + BASE_PROMPT


# === Example: OpenAI API ===
def openai_example(user_message: str):
    """Send a message with Trinity context via OpenAI API."""
    # pip install openai
    from openai import OpenAI

    client = OpenAI()  # Uses OPENAI_API_KEY env var
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content


# === Example: Anthropic API ===
def anthropic_example(user_message: str):
    """Send a message with Trinity context via Anthropic API."""
    # pip install anthropic
    from anthropic import Anthropic

    client = Anthropic()  # Uses ANTHROPIC_API_KEY env var
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message},
        ],
    )
    return response.content[0].text


# === Example: Generic HTTP (any API) ===
def generic_http_example(user_message: str, api_url: str, api_key: str):
    """Send a message with Trinity context via raw HTTP."""
    import json
    import urllib.request

    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    }
    req = urllib.request.Request(
        api_url,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


# === Session tracking ===
def record_session():
    """Record a session after interacting with the agent."""
    agent.start_session()
    agent.log_activity("Answered user questions via API")
    agent.add_learning("api_pattern", "Context prepend works across providers")
    agent.end_session()
    agent.observe("User prefers API-based integration", tags=["integration"])


if __name__ == "__main__":
    print("Trinity Pattern — Generic LLM Integration")
    print()
    print("System prompt with context:")
    print("-" * 40)
    print(system_prompt)
    print("-" * 40)
    print()
    print("This prompt can be sent to any LLM API.")
    print("See the function examples in this file for OpenAI, Anthropic, and generic HTTP.")
