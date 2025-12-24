# Demo: Customer Support Chatbot

## Approach

We built a customer support chatbot that integrates with an MCP server to help customers browse products and view orders.

### Authentication Decision

**Initial approach**: Require login (email + PIN) upfront before accessing the chat.

**Final approach**: No login screen. Authentication happens conversationally when needed.

### Why We Changed

| Upfront Login | Conversational Auth |
|---------------|---------------------|
| Extra UI complexity (login form + chat) | Single chat interface |
| Blocks users who just want to browse | Immediate access to product queries |
| Friction before value | Auth only when needed |

Most users want to browse products first. Only order-related queries require authentication. By deferring auth to the conversation, we:

1. Reduce friction for browsing
2. Simplify the UI to a single chat screen
3. Let the LLM agent handle the auth flow naturally

### How It Works

**Product queries** → Agent calls MCP tools directly → Returns results

**Order queries** → Agent asks for email + PIN → Verifies via MCP → Fetches orders

### Stack

- **LLM**: OpenAI GPT-3.5-turbo
- **Agent**: LangChain with MCP adapters
- **UI**: Gradio ChatInterface
- **Backend**: MCP server (Streamable HTTP)

