"""LangChain agent with MCP integration for customer support."""

import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()


class CustomerSupportAgent:
    MCP_SERVER_URL = "https://vipfapwm3x.us-east-1.awsapprunner.com/mcp"

    SYSTEM_MESSAGE = (
        "You are a helpful customer support chatbot for a company that sells computer products "
        "(monitors, printers, computers, etc.). Your role is to:\n"
        "- Help customers find products\n"
        "- Provide product information and details\n"
        "- Help customers view their order history\n"
        "- Answer questions about orders and products\n"
        "- Be friendly, professional, and concise\n"
        "\n"
        "You have access to the following tools:\n"
        "- search_products: Search for products by keyword\n"
        "- list_products: Browse products by category\n"
        "- get_product: Get detailed info for a specific product SKU\n"
        "- verify_customer_pin: Verify customer identity with email and 4-digit PIN\n"
        "- list_orders: List orders (requires customer_id from verify_customer_pin)\n"
        "- get_order: Get order details by order_id\n"
        "- get_customer: Get customer info (requires customer_id)\n"
        "- create_order: Create a new order (requires customer_id)\n"
        "\n"
        "IMPORTANT: For order-related requests:\n"
        "1. First ask the customer for their email and 4-digit PIN\n"
        "2. Use verify_customer_pin to authenticate them\n"
        "3. Extract the Customer ID from the response (it's a UUID like '41c2903a-f1a5-47b7-a81d-86b50ade220f')\n"
        "4. Use that Customer ID for list_orders, get_customer, or create_order\n"
        "\n"
        "Always provide clear, helpful responses. When showing product or order information, "
        "format it nicely for the user."
    )

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self._llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=api_key)
        self._mcp_client = MultiServerMCPClient(
            {
                "order-mcp": {
                    "transport": "http",
                    "url": self.MCP_SERVER_URL,
                }
            }
        )
        self._agent = None

    async def _initialize(self):
        if self._agent is None:
            tools = await self._mcp_client.get_tools()
            self._agent = create_agent(self._llm, tools)
        return self._agent

    def _convert_history(self, history: list) -> list:
        messages = []
        for item in history:
            if isinstance(item, dict):
                role = item.get("role", "")
                content = item.get("content", "")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))
            elif isinstance(item, (list, tuple)) and len(item) == 2:
                user_msg, assistant_msg = item
                messages.append(HumanMessage(content=user_msg))
                if assistant_msg:
                    messages.append(AIMessage(content=assistant_msg))
        return messages

    def _extract_response(self, response) -> str:
        if isinstance(response, dict):
            agent_messages = response.get("messages", [])
        elif isinstance(response, list):
            agent_messages = response
        else:
            agent_messages = []

        for msg in reversed(agent_messages):
            if isinstance(msg, AIMessage) and hasattr(msg, "content") and msg.content:
                return str(msg.content)

        return "I'm sorry, I couldn't generate a response."

    async def chat(self, message: str, history: list) -> str:
        if not message.strip():
            return ""

        agent = await self._initialize()

        messages = [SystemMessage(content=self.SYSTEM_MESSAGE)]
        messages.extend(self._convert_history(history))
        messages.append(HumanMessage(content=message))

        try:
            response = await agent.ainvoke({"messages": messages})
            return self._extract_response(response)
        except Exception as e:
            return f"I encountered an error: {str(e)}"

