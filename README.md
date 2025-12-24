# Customer Support Chatbot with MCP Integration

A prototype customer support chatbot for a company that sells computer products (monitors, printers, etc.). The chatbot integrates with an MCP (Model Context Protocol) server to provide customers with product information, order management, and support services.

## Problem Statement

Build a customer support chatbot that:
- Helps customers find products (monitors, printers, etc.)
- Allows customers to view their order history
- Provides product details and information
- Integrates with an external MCP server via Streamable HTTP
- Uses a cost-effective LLM (GPT-3.5-turbo)
- Provides a simple, user-friendly interface (Gradio)
- Authenticates customers using email and PIN

## Solution Approach

### Architecture Overview

```
┌─────────────────┐
│   Gradio UI     │  (Login Form + Chat Interface)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ LangChain Agent  │  (Agent Orchestration + Tool Calling)
└────────┬────────┘
         │
         ├──────────────┐
         ▼              ▼
┌─────────────┐  ┌──────────────────┐
│   OpenAI    │  │  MCP Adapters    │
│ GPT-3.5-turbo│  │ (langchain-mcp) │
│             │  └────────┬─────────┘
└─────────────┘           │
                          ▼
                  ┌──────────────┐
                  │  MCP Server  │
                  │ (Streamable  │
                  │    HTTP)     │
                  └──────────────┘
```

### Key Design Decisions

1. **Simple Chat Interface**: No login screen
   - Users interact directly with the chatbot
   - Authentication happens conversationally when needed
   - Agent asks for email + PIN for order-related queries

2. **LLM Integration**: LangChain Agents with MCP Adapters
   - Uses LangChain v1 agents for orchestration
   - Leverages `langchain-mcp-adapters` for seamless MCP server integration
   - LangChain agents automatically handle tool selection and execution
   - Agent manages authentication flow conversationally

3. **UI Framework**: Gradio ChatInterface
   - Simple, fast to implement
   - Built-in chat interface with examples
   - Easy deployment to HuggingFace Spaces

4. **MCP Integration**: LangChain MCP Adapters
   - Uses `MultiServerMCPClient` from `langchain-mcp-adapters`
   - Supports HTTP transport for MCP servers
   - Automatic tool discovery and conversion to LangChain tools

### MCP Server Capabilities

The MCP server (`order-mcp` v1.22.0) provides the following tools:

- **Authentication**:
  - `verify_customer_pin`: Authenticate customer with email + PIN

- **Products**:
  - `list_products`: Browse products with optional filters (category, active status)
  - `get_product`: Get detailed product information by SKU
  - `search_products`: Search products by name or description

- **Orders**:
  - `list_orders`: List orders with filters (customer_id, status)
  - `get_order`: Get detailed order information
  - `create_order`: Create new orders (not in MVP scope)

- **Customers**:
  - `get_customer`: Get customer information by UUID

### Implementation Flow

1. **Product Queries** (no auth):
   ```
   User asks about products → Agent calls search_products/list_products/get_product → 
   Returns formatted product info
   ```

2. **Order Queries** (requires auth):
   ```
   User asks about orders → Agent asks for email + PIN → 
   Agent calls verify_customer_pin → Extracts customer_id → 
   Agent calls list_orders with customer_id → Returns order info
   ```

3. **Agent Execution Process**:
   - LangChain agent receives user message
   - Agent decides which MCP tools to call (if any)
   - For authenticated operations, agent manages the verification flow
   - MCP tools are executed via langchain-mcp-adapters
   - Agent processes tool results and generates natural language response

## Project Structure

```
chatbot_mcp/
├── src/
│   ├── __init__.py        # Package marker
│   ├── agent.py           # MCP client + LangChain agent + chat logic
│   └── main.py            # Gradio UI entry point
├── requirements.txt       # Python dependencies (legacy, use pyproject.toml)
├── .env                   # Environment variables (OPENAI_API_KEY)
├── pyproject.toml         # Project configuration and dependencies (used by uv)
└── README.md              # This file
```

## Setup

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager (install with: `curl -LsSf https://astral.sh/uv/install.sh | sh` or `pip install uv`)
- OpenAI API key
- Access to MCP server: `https://vipfapwm3x.us-east-1.awsapprunner.com/mcp`

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd chatbot_mcp
   ```

2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```
   
   This will:
   - Create a virtual environment automatically
   - Install all dependencies from `pyproject.toml`
   - Set up the project environment

3. Set up environment variables:
   ```bash
   # Create .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   # Or manually create .env file and add: OPENAI_API_KEY=your_key_here
   ```

4. Run the application:
   ```bash
   uv run python src/main.py
   ```
   
   Alternatively, activate the virtual environment and run directly:
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   python src/main.py
   ```

## Usage

Open the app in your browser at `http://localhost:7860` and start chatting!

### Sample Queries

#### Product Queries (No authentication required)

| Query | Description |
|-------|-------------|
| "Show me monitors" | Search for monitors |
| "What products do you have?" | List all products |
| "Search for gaming laptops" | Search by keyword |
| "Tell me about product COM-0001" | Get details for specific SKU |
| "What printers are available?" | Search for printers |
| "List all computers" | Browse by category |
| "What's the price of MON-0054?" | Get product pricing |

#### Order Queries (Requires authentication)

For order-related queries, you'll need to provide your email and PIN:

| Query | Description |
|-------|-------------|
| "What are my orders?" | Agent will ask for email + PIN, then show orders |
| "Check my order status" | View order statuses |
| "Show my order history" | List past orders |

**Example conversation for orders:**
```
You: What are my orders?
Bot: I'd be happy to help you view your orders. Could you please provide your email and 4-digit PIN for verification?
You: My email is donaldgarcia@example.net and PIN is 7912
Bot: ✓ Customer verified: Donald Garcia. Here are your orders: [order list]
```

#### Combined Queries

| Query | Description |
|-------|-------------|
| "I'm looking for a 27-inch monitor under $500" | Product search with criteria |
| "Do you have any gaming keyboards in stock?" | Check availability |
| "What's your best-selling printer?" | Product recommendation |
| "I need help choosing a monitor for video editing" | Get recommendations |

## Development

### Using uv

This project uses [uv](https://github.com/astral-sh/uv) for fast and reliable dependency management.

**Common commands:**
- `uv sync` - Install dependencies and create virtual environment
- `uv run python app.py` - Run the app using uv's managed environment
- `uv add <package>` - Add a new dependency
- `uv remove <package>` - Remove a dependency
- `uv lock` - Update the lock file (if using uv.lock)

**Activating the virtual environment:**
After running `uv sync`, activate the environment:
```bash
source .venv/bin/activate  # On macOS/Linux
.venv\Scripts\activate      # On Windows
```

## Test Data

The following test customers are available for testing:

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

## MCP Server Details

- **URL**: `https://vipfapwm3x.us-east-1.awsapprunner.com/mcp`
- **Protocol**: JSON-RPC 2.0 over HTTP
- **Server**: `order-mcp` v1.22.0
- **Authentication**: Required for order-related operations (email + PIN)

## Technology Stack

- **LLM**: OpenAI GPT-3.5-turbo via LangChain
- **Agent Framework**: LangChain v1 agents
- **MCP Integration**: langchain-mcp-adapters
- **UI Framework**: Gradio
- **Package Manager**: uv
- **Language**: Python 3.12+

## Future Enhancements

- Deploy to HuggingFace Spaces
- Add support for creating orders
- Implement conversation persistence
- Add more sophisticated error handling
- Support for multiple languages
- Integration with additional MCP tools

## License

[Add license information]

