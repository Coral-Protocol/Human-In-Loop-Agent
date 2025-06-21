## [Human-in-the-Loop Communication Agent](https://github.com/Coral-Protocol/Human-In-Loop-Agent)

A communication agent that responds with requested fun content(joke/quote/fact) incorporating a human-in-the-loop for oversight..

## Responsibility
A communication agent that waits for messages from other agents and responds with requested fun content(joke/quote/fact). Built with human-in-the-loop confirmation using [Agno framework](https://docs.agno.com/introduction).

## Details
- **Framework**: Agno Agent Framework
- **Tools used**: Coral Tools, generate_joke, generate_quote, generate_fact
- **AI model**: GPT-4o
- **Date added**: June 2025
- **Reference**: [Human-In-Loop-Agent Repo](https://github.com/Arindam200/awesome-ai-apps/tree/main/simple_ai_agents/human_in_the_loop_agent)
- **License**: MIT 


## Use the Agent  

### 1. Clone & Install Dependencies


<details>  

Ensure that the [Coral Server](https://github.com/Coral-Protocol/coral-server) is running on your system. If you are trying to run Human-in-the-Loop agent and require coordination with other agents, you can run the [Interface Agent](https://github.com/Coral-Protocol/Coral-Interface-Agent) on the Coral Server to interact with this agent

```bash
# In a new terminal clone the repository:
git clone https://github.com/Coral-Protocol/Human-In-Loop-Agent.git

# Navigate to the project directory:
cd Human-In-Loop-Agent

# Install `uv`:
pip install uv

# Install dependencies from `pyproject.toml` using `uv`:
uv sync

```

</details>
 

### 2. Configure Environment Variables

<details>
 
Get the API Key:
[OpenAI](https://platform.openai.com/api-keys)


```bash
# Create .env file in project root
cp -r .env_sample .env
```
</details>


### 3. Run Agent

<details>

```bash
# Run the agent using `uv`:
uv run python main.py
```
</details>


### 4. Example

<details>


```bash
# Setup:
1. Launch the Interface agent: https://github.com/Coral-Protocol/Coral-Interface-Agent
2. Run the Human in loop agent
3. Ask the interface agent to "ask the human in loop agent to get me a fact/joke/quote"

#Output:
The Human-in-the-Loop agent will respond with appropriate content after user confirmation.
```
</details>


## Choice Explanation
- **y**: Yes, accept the response and run the tool
- **n**: Do not accept the response and do not run the tool  
- **retry**: Retry running the tool again for better response


## Creator Details
- **Name**: Ahsen Tahir
- **Affiliation**: Coral Protocol
- **Contact**: [Discord](https://discord.com/invite/Xjm892dtt3)
