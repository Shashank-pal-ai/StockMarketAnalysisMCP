import os
import asyncio
import argparse
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.chat_models import init_chat_model
from langgraph_supervisor import create_supervisor
from agents import create_agents
from utils import pretty_print_messages
from config import MODEL_NAME, SUPERVISOR_PROMPT

# Load environment variables from .env file
load_dotenv()

async def run_agent(query):
    """
    Runs the multi-agent stock analysis system.
    """
    try:
        # Check for required environment variables
        if not os.getenv("BRIGHT_DATA_API_TOKEN") or not os.getenv("OPENAI_API_KEY"):
            raise ValueError("BRIGHT_DATA_API_TOKEN and OPENAI_API_KEY must be set.")

        # Initialize the client for tools
        client = MultiServerMCPClient(
            {
                "bright_data": {
                    "command": "npx",
                    "args": ["@brightdata/mcp"],
                    "env": {
                        "API_TOKEN": os.getenv("BRIGHT_DATA_API_TOKEN"),
                        "WEB_UNLOCKER_ZONE": os.getenv("WEB_UNLOCKER_ZONE", "unblocker"),
                        "BROWSER_ZONE": os.getenv("BROWSER_ZONE", "scraping_browser"),
                    },
                    "transport": "stdio",
                },
            }
        )
        tools = await client.get_tools()

        # Initialize the language model
        model = init_chat_model(model=MODEL_NAME, api_key=os.getenv("OPENAI_API_KEY"))

        # Create the agents
        agents = create_agents(model, tools)

        # Create the supervisor
        supervisor = create_supervisor(
            model=model,
            agents=agents,
            prompt=SUPERVISOR_PROMPT,
            add_handoff_back_messages=True,
            output_mode="full_history",
        ).compile()

        # Stream the conversation
        for chunk in supervisor.stream(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": query,
                    }
                ]
            },
        ):
            pretty_print_messages(chunk, last_message=True)

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """
    Main function to run the script.
    """
    parser = argparse.ArgumentParser(description="Run the multi-agent stock analysis system.")
    parser.add_argument(
        "query",
        type=str,
        nargs="?",
        default="Give me good stock recommendation from NSE",
        help="The query to send to the agent.",
    )
    args = parser.parse_args()

    asyncio.run(run_agent(args.query))

if __name__ == "__main__":
    main()