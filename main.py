from typing import List
from pydantic import BaseModel, Field

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from tavily import TavilyClient

load_dotenv()
tavily = TavilyClient()

class SearchResult(BaseModel):
    """ Schema for the search result """

    city: str = Field(description="The city the weather is for")
    weather: str = Field(description="The weather in the city, including the temperature, humidity, and wind speed and any other relevant weather information")

class AgentResponse(BaseModel):
    """ Schema for the agent response """

    search_results: List[SearchResult] = Field(default_factory=list, description="The search results for the cities")

@tool
def search(query: str) -> str:
    """
    Tool that searches over the internet
    Args:
        city: The query to search the internet for
    Returns:
        The search result
    """
    print(f"Searching for {query}")
    return tavily.search(query=query)


# llm = ChatOpenAI(model="gpt-5.6-luna", reasoning_effort="none")
llm = init_chat_model(model="gpt-5.6-luna", reasoning_effort="none") # better abstraction to initialize the model
tools = [search]
agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)


def main():
    print("Hello from search-agent!")
    result = agent.invoke(
        {
            "messages": HumanMessage(
                content="What is the weather in Toronto ON and Agra, India?"
            )
        }
    )

    print(result['structured_response'])


if __name__ == "__main__":
    main()
