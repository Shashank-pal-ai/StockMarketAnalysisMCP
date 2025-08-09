from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from config import (
    MODEL_NAME,
    STOCK_FINDER_AGENT_PROMPT,
    MARKET_DATA_AGENT_PROMPT,
    NEWS_ANALYST_AGENT_PROMPT,
    PRICE_RECOMMENDER_AGENT_PROMPT,
    SUPERVISOR_PROMPT,
)

def agent_creator(model, tools, prompt, name):
    """Factory function to create a new agent."""
    return create_react_agent(model, tools, prompt=prompt, name=name)

def create_agents(model, tools):
    """Creates all the agents for the stock analysis task."""
    stock_finder_agent = agent_creator(
        model,
        tools,
        STOCK_FINDER_AGENT_PROMPT,
        "stock_finder_agent",
    )
    market_data_agent = agent_creator(
        model,
        tools,
        MARKET_DATA_AGENT_PROMPT,
        "market_data_agent",
    )
    news_analyst_agent = agent_creator(
        model,
        tools,
        NEWS_ANALYST_AGENT_PROMPT,
        "news_analyst_agent",
    )
    price_recommender_agent = agent_creator(
        model,
        tools,
        PRICE_RECOMMENDER_AGENT_PROMPT,
        "price_recommender_agent",
    )
    return [
        stock_finder_agent,
        market_data_agent,
        news_analyst_agent,
        price_recommender_agent,
    ]
