# Customer Support Chatbot

A customer support chatbot for computer products using LangChain agents and MCP.

## Quick Start

```bash
uv sync
cp .env.example .env  # Add your OpenAI API key
uv run src/main.py
```

Open http://localhost:7860

## Sample Queries

**Products** (no auth):
- "Show me monitors"
- "What products do you have?"
- "Tell me about product COM-0001"

**Orders** (requires email + PIN):
- "What are my orders?"
- "Check my order status"

## Test Credentials

| Email | PIN |
|-------|-----|
| donaldgarcia@example.net | 7912 |
| michellejames@example.com | 1520 |
| laurahenderson@example.org | 1488 |
| spenceamanda@example.org | 2535 |
| glee@example.net | 4582 |
| williamsthomas@example.net | 4811 |
| justin78@example.net | 9279 |
| jason31@example.com | 1434 |
| samuel81@example.com | 4257 |
| williamleon@example.net | 9928 |

## Stack

- **LLM**: OpenAI GPT-3.5-turbo
- **Agent**: LangChain + langchain-mcp-adapters
- **UI**: Gradio
- **MCP Server**: `https://vipfapwm3x.us-east-1.awsapprunner.com/mcp`

## Documentation

- [Architecture](ARCHITECTURE.md) - Design decisions and system overview
