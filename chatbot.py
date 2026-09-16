import os
import uuid
import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
import gradio as gr


load_dotenv()


if not os.getenv("HF_TOKEN"):
    raise ValueError("Must provide HF_TOKEN environment variable")


llm = ChatOpenAI(
    model="Qwen/Qwen3-8B",
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)


async def chatbot():
    """Create a LangGraph ReAct agent with MCP tools."""

    mcp_client = MultiServerMCPClient(
        {
            "ShoppingList": {
                "url": "http://localhost:8000/mcp",
                "transport": "sse",
            }
        }
    )

    tools = await mcp_client.get_tools()

    prompt = """
    You are a helpful assistant that lets users manage their shopping
    lists using the available ShoppingList tools.

    Use the tools whenever the user wants to:
    - create a shopping list
    - view shopping lists
    - add shopping items
    - update shopping items
    - delete shopping lists or items
    - mark items as completed

    IMPORTANT:
    When creating a shopping list, the description must always be a string.
    If the user does not provide a description, use an empty string "".
    Never send null for the description.
    """

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=prompt
    )

    thread_id = str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }


    async def chat_with_agent(message, history):
        """Send the user's message to the LangGraph agent."""

        agent_input = {
            "messages": history + [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }

        result = await agent.ainvoke(
            agent_input,
            config
        )

        return result["messages"][-1].content


    chat_interface = gr.ChatInterface(
        fn=chat_with_agent,
        title="🤖 Shopping List Agent",
        description="Chat with an AI agent that can manage your shopping list.",
        examples=[
            "I need to buy a watermelon",
            "What's in my shopping list?",
            "Let's add spaghetti and tomato sauce",
            "I just bought the watermelon",
            "Remove the tomato sauce",
            "I need an extra spaghetti",
        ]
    )

    chat_interface.launch()


if __name__ == "__main__":
    asyncio.run(chatbot())