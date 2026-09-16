# Shopping List AI Agent — FastAPI + MCP + LangGraph

An AI-powered Shopping List application that allows users to manage shopping lists and items through natural language.

The project combines **FastAPI**, **SQLAlchemy**, **Model Context Protocol (MCP)**, **LangGraph/LangChain Agents**, **Hugging Face LLMs**, and **Gradio** to create an AI agent capable of interacting with a real backend API.

Instead of manually calling REST API endpoints, users can simply communicate with the AI agent using natural language.

For example:

> "Create a shopping list called Grocery List and add 2 kg of apples and 1 litre of milk."

The AI agent understands the request and uses the appropriate backend tools to perform these operations.

---

## Features

- Create, read, update, and delete shopping lists
- Add, update, retrieve, and delete shopping items
- Mark shopping items as completed
- Retrieve shopping lists with their associated items
- Natural-language interaction through an AI agent
- FastAPI REST API
- Automatic MCP tool generation from FastAPI endpoints
- Async database operations using SQLAlchemy
- SQLite database for local development
- Gradio-based chatbot interface
- Hugging Face LLM integration
- Agent-based tool calling using LangGraph/LangChain

---

# Architecture

The project consists of two major parts:

### 1. FastAPI Backend

The FastAPI application provides the actual shopping-list functionality.

It communicates with the SQLite database through SQLAlchemy and exposes operations such as:

- Create shopping list
- Get shopping lists
- Update shopping list
- Delete shopping list
- Create shopping item
- Get shopping items
- Update shopping item
- Delete shopping item
- Toggle item completion

### 2. AI Agent

The chatbot acts as an intelligent interface over the FastAPI backend.

The agent receives a user's natural-language request, decides which tool is required, calls the corresponding MCP tool, and returns the result to the user.

---

## 🔄 How FastAPI, MCP and LangGraph Work Together

The main architecture can be represented as:

```text
                    User
                      │
                      ▼
              ┌───────────────┐
              │    Gradio     │
              │ Chat Interface│
              └───────┬───────┘
                      │
              Natural Language
                      │
                      ▼
              ┌───────────────┐
              │  AI Agent     │
              │ LangGraph /   │
              │ LangChain     │
              └───────┬───────┘
                      │
                 Tool Selection
                      │
                      ▼
              ┌───────────────┐
              │ MCP Client    │
              │               │
              │ Discovers and │
              │ calls tools   │
              └───────┬───────┘
                      │
                MCP / SSE
                      │
                      ▼
              ┌───────────────┐
              │   FastAPI     │
              │   MCP Server  │
              └───────┬───────┘
                      │
                API Endpoints
                      │
                      ▼
              ┌───────────────┐
              │ CRUD Layer    │
              │  SQLAlchemy   │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ SQLite DB     │
              └───────────────┘
