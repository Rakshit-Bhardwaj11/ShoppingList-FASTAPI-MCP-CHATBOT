import os
import uuid

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

load_dotenv()

if not os.getenv("HF_TOKEN"):
    raise ValueError("HF_TOKEN environment variable is not set")


async def create_shopping_agent():

    llm = ChatOpenAI(
        model="Qwen/Qwen3-8B",
        base_url="https://router.huggingface.co/v1",
        api_key=os.getenv("HF_TOKEN"),
    )

    mcp_client = MultiServerMCPClient(
        {
            "ShoppingList": {
                "url": "https://shopping-list-fastapi-mcp.onrender.com/mcp",,
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

    Always use the available tools to perform operations instead of
    pretending that an operation was completed.
    """

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=prompt,
    )

    return agent
