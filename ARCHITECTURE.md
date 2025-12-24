# Architecture

## Overview

```
┌─────────────────┐
│   Gradio UI     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ LangChain Agent │
└────────┬────────┘
         │
         ├──────────────┐
         ▼              ▼
┌─────────────┐  ┌──────────────────┐
│   OpenAI    │  │  MCP Adapters    │
│ GPT-3.5-turbo│  │ (langchain-mcp) │
└─────────────┘  └────────┬─────────┘
                          │
                          ▼
                  ┌──────────────┐
                  │  MCP Server  │
                  └──────────────┘
```

## Design Decisions

### Conversational Authentication

No login screen. The agent asks for email + PIN only when the user requests order details.

| Upfront Login | Conversational Auth |
|---------------|---------------------|
| Extra UI (login + chat) | Single chat interface |
| Blocks browsers | Immediate product access |
| Friction first | Auth only when needed |

### LangChain + MCP

- `MultiServerMCPClient` connects to MCP server
- Tools auto-discovered and converted to LangChain tools
- Agent decides which tools to call based on user intent

## MCP Tools

| Tool | Auth Required | Description |
|------|---------------|-------------|
| `search_products` | No | Search by keyword |
| `list_products` | No | Browse products |
| `get_product` | No | Get product by SKU |
| `verify_customer_pin` | - | Authenticate user |
| `list_orders` | Yes | List customer orders |
| `get_order` | Yes | Get order details |
| `get_customer` | Yes | Get customer info |
| `create_order` | Yes | Create new order |

## Flow

**Products**: User → Agent → MCP tool → Response

**Orders**: User → Agent asks for credentials → `verify_customer_pin` → `list_orders` → Response

## Project Structure

```
├── app.py      # Gradio UI entry point
└── agent.py    # LangChain agent + MCP client
```

