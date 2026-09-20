# langchain-search-agent

A LangChain agent that answers weather questions by searching the live web with Tavily, then returns the results as typed, structured data instead of free-form text. Ask it about two cities and it decides on its own to search twice.

## What it does
- Exposes a Tavily-backed `search` tool to the agent
- Runs an agent loop that picks when and how often to search
- Returns a validated `AgentResponse` Pydantic object with one entry per city

## Notes & details
- **The docstring *is* the tool spec** — the `@tool` decorator turns a plain function into a tool, and the model reads the docstring and type hints to decide when to call it. Vague docstring, vague tool use.
- **Structured output** — `response_format=AgentResponse` makes the agent conform to a Pydantic schema, so you read `result['structured_response']` and get real objects rather than parsing prose.
- **`init_chat_model` over `ChatOpenAI`** — a provider-agnostic way to spin up a model; swapping providers becomes a string change. The direct `ChatOpenAI` line is left commented out for comparison.
- **Agentic, not a fixed chain** — nothing in the code says "search twice." The sample prompt asks about Toronto and Agra, and the agent loops until it has both.
- **`reasoning_effort="none"`** trades deliberation for latency, which is fine for lookups like this.
- **Requires** `OPENAI_API_KEY` and `TAVILY_API_KEY` in `.env`.
- The `print` inside the tool is a cheap way to watch what the agent actually decided to query.

## Run
```bash
uv sync
uv run main.py
```
