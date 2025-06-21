import os
import urllib.parse
import asyncio
from typing import Iterator
from agno.agent import Agent
from agno.exceptions import RetryAgentRun, StopAgentRun
from agno.models.openai import OpenAIChat
from agno.tools import FunctionCall, tool
from agno.tools.mcp import MCPTools
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
import json

load_dotenv()
console = Console()
 # MCP Server configuration
base_url = os.getenv("CORAL_SSE_URL")
params = {
    "waitForAgents": 2,
    "agentId": os.getenv("AGENT_ID"),
    "agentDescription": "You are a helpful human in loop agent."
}
query_string = urllib.parse.urlencode(params)
MCP_SERVER_URL = f"{base_url}?{query_string}"
MAX_RETRIES = 3
retry_counter = {"count": 0}  # For mutable retry count inside hook

# Pre-hook shared across all tools
def pre_hook(fc: FunctionCall):
    live = console._live # type: ignore
    live.stop() # type: ignore

    console.print(f"\n🔍 [bold]Preparing to run:[/bold] [cyan]{fc.function.name}[/cyan]")
    console.print(f"📦 [bold]Arguments:[/bold] {fc.arguments}")

    choice = (Prompt.ask(
        "\n🤔 Do you want to continue?",
        choices=["y", "n", "retry"],
        default="y"
    ).strip().lower())

    live.start() # type: ignore

    if choice == "n":
        console.print("❌ [red]Operation cancelled by user.[/red]")
        raise StopAgentRun("Cancelled by user", agent_message="I don't have any tool calls to make.")

    if choice == "retry":
        retry_counter["count"] += 1
        if retry_counter["count"] >= MAX_RETRIES:
            console.print("❌ [red]Maximum retries reached.[/red]")
            raise StopAgentRun("Too many retries", agent_message="Stopped after several retries.")
        console.print(f"🔄 [yellow]Retrying... (Attempt {retry_counter['count']} of {MAX_RETRIES})[/yellow]")
        raise RetryAgentRun("Retrying with new data", agent_message="Let me try again!")
    
    # Reset retry counter when user chooses to continue
    retry_counter["count"] = 0

# Tool 1: Get an interesting fact
@tool(pre_hook=pre_hook)
def get_fact(fact: str) -> Iterator[str]:
    yield fact

# Tool 2: Get a motivational quote
@tool(pre_hook=pre_hook)
def get_quote(quote: str) -> Iterator[str]:
    yield quote

# Tool 3: Get a joke
@tool(pre_hook=pre_hook)
def get_joke(joke: str) -> Iterator[str]:
    yield joke

# Initialize the agent
async def main():
    async with MCPTools(url=MCP_SERVER_URL, transport="sse", timeout_seconds=60) as coral_tools:
        agent = Agent(
            description="An agent that waits for messages from other agents and responds with fun content.",
            instructions="""
            You are a communication agent that ONLY waits for messages from other agents and responds with requested fun content.

            CRITICAL WORKFLOW - Follow this exactly:
            
            1. FIRST, call the list_agents tool to discover and learn about all available agents in the system
            2. THEN, start by using ONLY the wait_for_mentions tool to listen for incoming messages
            3. DO NOT use any other tools until you receive a message from another agent
            4. Keep calling wait_for_mentions repeatedly until you get a message
            
            5. When you receive a message from another agent, analyze what they're requesting:
               - If they ask for a "fact" or "fun fact" → call get_fact tool with an interesting educational fact
               - If they ask for a "quote" or "motivational quote" → call get_quote tool with an inspiring quote  
               - If they ask for a "joke" → call get_joke tool with a funny, light-hearted joke
               - If they ask for something else → just acknowledge politely without using content tools
            
            6. After generating the requested content with the appropriate tool, use send_msg tool to send the response back to the agent who requested it. IMPORTANT: Include the name/ID of the requesting agent in the mentions parameter of send_msg
            
            7. Immediately return to step 2 and continue waiting for more mentions
            
            IMPORTANT RULES:
            - Always start by calling list_agents tool first to discover available agents
            - Then start with wait_for_mentions tool and keep using it until you get a message
            - Only use get_fact, get_quote, or get_joke tools AFTER receiving a specific request
            - Always send responses back using send_msg tool with the requesting agent's name in the mentions parameter
            - Create high-quality, engaging content when requested:
              * Facts: Fascinating, educational, and surprising information
              * Quotes: Inspirational, meaningful, and motivational messages
              * Jokes: Clean, clever, and genuinely funny content
            - Continue the loop indefinitely unless explicitly stopped
            """,
            tools=[get_fact, get_quote, get_joke, coral_tools],
            markdown=True,
            model=OpenAIChat(
                id="gpt-4o",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        )

        # Start the continuous communication loop
        console.print("🚀 [bold green]Starting communication agent...[/bold green]")
        console.print("📡 [yellow]Agent is now waiting for mentions from other agents...[/yellow]")
        
        while True:
            try:
                retry_counter["count"] = 0
                await agent.aprint_response(
                    "When you receive a message, print the response by the wait for mentions tool and call the tool to generate appropriate fun content (fact, quote, or joke) and send it back to the sender agent. Then continue waiting for more mentions.",
                    
                    stream=True, 
                    console=console,
                    show_full_reasoning=True
                )
                
                # Brief pause before next iteration
                await asyncio.sleep(1)
                
            except KeyboardInterrupt:
                console.print("\n👋 [bold red]Shutting down communication agent...[/bold red]")
                break
            except Exception as e:
                console.print(f"\n⚠️ [bold yellow]Error occurred: {str(e)}[/bold yellow]")
                console.print("🔄 [yellow]Restarting in 5 seconds...[/yellow]")
                await asyncio.sleep(5)

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
