import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langgraph_supervisor import create_supervisor


load_dotenv()
from langchain_core.messages import convert_to_messages

async def run_agent():
    try:
        print("hello")
        client = MultiServerMCPClient(
            {
                "bright_data": {
                    "command": "npx",
                    "args": ["@brightdata/mcp"],
                    "env": {
                        "API_TOKEN": os.getenv("BRIGHT_DATA_API_TOKEN"),
                    },
                    "transport": "stdio",
                }
            }
        )
        tools = await client.get_tools()
        model = init_chat_model(
            model="openai:gpt-4.1", api_key=os.getenv("OPENAI_API_KEY")
        )
        agent = create_react_agent(
            model,
            tools,
            prompt="You are a web search agent with access to brightdata tool to get the latest data",
        )
        agent_response = await agent.ainvoke({"messages": "Flights from New Delhi to Zurich on Dec 1 2025"})
        print(agent_response["messages"][-1].content)
    except Exception as e:
        print(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    asyncio.run(run_agent())
