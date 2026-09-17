# Shopping List FASTAPI MCP Chatbot

An AI-powered shopping list management application that allows users to create, view, update, and delete shopping lists and items using natural language.

The project integrates **Streamlit, LangGraph, LangChain, MCP, FastAPI, SQLAlchemy, Hugging Face, and SQLite** to demonstrate how an AI agent can interact with backend services through MCP tools.

## Live Deployment

### AI Chatbot — Streamlit
https://shoppinglist-fastapi-mcp-chatbot.streamlit.app/

### FastAPI + MCP Backend — Render
https://shopping-list-fastapi-mcp.onrender.com/

## Project Overview

Instead of manually interacting with API endpoints, users can manage their shopping lists using simple natural-language instructions.

For example:

> Create a shopping list called "Weekend Shopping".

> Add 2 kg of apples and 1 litre of milk to Weekend Shopping.

> Mark the milk as completed.

The AI agent understands the user's request, selects the appropriate MCP tool, and performs the required operation through the FastAPI backend.

## Architecture

```text
                         User
                           │
                           ▼
                  ┌─────────────────┐
                  │    Streamlit    │
                  │  Chat Interface │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │    AI Agent     │
                  │ LangGraph /     │
                  │ LangChain       │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   MCP Client    │
                  │  Tool Discovery │
                  └────────┬────────┘
                           │
                        MCP / SSE
                           │
                           ▼
                  ┌─────────────────┐
                  │     FastAPI     │
                  │    MCP Server   │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │    CRUD Layer   │
                  │    SQLAlchemy   │
                  └────────┬────────┘
                           │
                           ▼
                     ┌───────────┐
                     │  SQLite   │
                     │  Database │
                     └───────────┘
