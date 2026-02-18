# Generic LLM — Trinity Pattern Integration

Prepend Trinity context to any LLM API call for persistent identity.

## The Pattern

```python
from trinity_pattern import Agent

agent = Agent(directory="./my_agent")
context = agent.get_context()

# Prepend to any system prompt
messages = [
    {"role": "system", "content": context + "\n---\n" + your_base_prompt},
    {"role": "user", "content": user_input},
]
```

## Supported APIs

The example script shows integration with:
- **OpenAI** (GPT-4, GPT-3.5)
- **Anthropic** (Claude)
- **Any HTTP API** (generic chat completion endpoints)

## Usage

```bash
pip install trinity-pattern
python3 api_prepend.py
```

The script prints the combined system prompt so you can see exactly what gets
sent to the LLM. Adapt the function examples to your application.
