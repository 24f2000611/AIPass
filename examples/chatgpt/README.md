# ChatGPT — Trinity Pattern Integration

Give ChatGPT persistent memory using Trinity Pattern custom instructions.

## Setup

1. Install trinity-pattern:
   ```bash
   pip install trinity-pattern
   ```

2. Generate your context:
   ```bash
   python3 generate_context.py --name "MyBot" --role "Writing Assistant"
   ```

3. Copy the output and paste it into:
   **ChatGPT → Settings → Personalization → Custom Instructions**

## Updating

After each session, update your Trinity files (manually or via script), then
re-run `generate_context.py` to get the latest context for your next session.

## How It Works

Trinity files live on your machine. The script reads them and formats a context
string that tells ChatGPT who it is, what it's done recently, and how you
prefer to collaborate. ChatGPT sees this at the start of every conversation.
