"""Gradio UI entry point for Customer Support Chatbot."""

import asyncio
import gradio as gr
from agent import CustomerSupportAgent

agent = CustomerSupportAgent()


def chat_response(message: str, history: list) -> str:
    return asyncio.run(agent.chat(message, history))


demo = gr.ChatInterface(
    fn=chat_response,
    title="🛒 Customer Support Assistant",
    description=(
        "Welcome! I'm here to help you:\n\n"
        "• 🔍 Search for products\n"
        "• ℹ️ Get product details and pricing\n"
        "• 📦 View order history (requires email + PIN verification)\n"
        "• ❓ Answer questions about products"
    ),
    examples=[
        "Show me monitors",
        "What products do you have?",
        "What are my orders?",
    ],
)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Soft())
