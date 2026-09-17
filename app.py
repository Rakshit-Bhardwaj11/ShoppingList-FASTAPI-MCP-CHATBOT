import asyncio
import streamlit as st

from agent import create_shopping_agent


st.set_page_config(
    page_title="Shopping List AI Agent",
    page_icon="🛒",
    layout="centered",
)


st.title("🛒 Shopping List AI Agent")
st.caption(
    "Manage your shopping lists using natural language "
    "with LangGraph, MCP and FastAPI."
)


if "messages" not in st.session_state:
    st.session_state.messages = []


async def run_agent():
    agent = await create_shopping_agent()

    result = await agent.ainvoke(
        {
            "messages": st.session_state.messages
        }
    )

    return result


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_input = st.chat_input(
    "What would you like to do?"
)


if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            result = asyncio.run(run_agent())

            response = result["messages"][-1].content

            st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )