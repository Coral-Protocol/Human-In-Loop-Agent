# Human-in-the-Loop Communication Agent

## Responsibility:
A communication agent that waits for messages from other agents and responds with requested fun content(joke/quote/fact). Built with human-in-the-loop confirmation using [Agno framework](https://docs.agno.com/introduction).

## Details
- **Framework**: Agno Agent Framework
- **Tools Used**: Coral Tools, generate_joke, generate_quote, generate_fact
- **AI Model**: GPT-4o  
- **Date Added**: June 2025
- **License**: MIT

## Install Dependencies
```bash
pip install uv
uv sync
```

## Configure Environment Variables
Create a `.env` file in the project root and add your credentials:

```bash
# Required environment variables:
OPENAI_API_KEY=your_openai_api_key_here
```

## Run Agent
Run the agent:

```bash
uv run python main.py
```

## Agent Capabilities
- **Human-in-the-Loop Confirmation** – User approval system for all tool calls with retry functionality  
- **Content Generation** – Provides facts, motivational quotes, and jokes upon request

## Workflow
1. **Discovery Phase**: Lists all available agents in the system
2. **Listening Phase**: Continuously waits for mentions from other agents
3. **Content Generation**: Responds to requests with appropriate content:
   - Facts
   - Quotes  
   - Jokes
4. **Response Delivery**: Sends generated content back to the requesting agent
5. **Loop Continuation**: Returns to listening for more mentions

## Choice Explanation
- **y**: Yes, accept the response and run the tool
- **n**: Do not accept the response and do not run the tool  
- **retry**: Retry running the tool again for better response


## Example Usage
1. Launch the [Interface agent](https://github.com/Coral-Protocol/Coral-Interface-Agent)
2. Run the Human in loop agent
3. Ask the interface agent to "ask the human in loop agent to get me a fact/joke/quote"
4. The interface agent will ask the human in loop agent and then the Human in loop agent will get the response back

## Creator Details
- **Name**: Ahsen Tahir
- **Contact**: ahsen.t@coralprotocol.org
- **Source**: Based on [awesome-ai-apps](https://github.com/Arindam200/awesome-ai-apps/tree/main/simple_ai_agents/human_in_the_loop_agent)
