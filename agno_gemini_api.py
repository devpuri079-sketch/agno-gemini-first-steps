from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv

load_dotenv()

# Using Google AI Studio
agent = Agent(
    model=Gemini(id="gemini-2.0-flash"),
    markdown=True,
)


# Print the response in the terminal
agent.print_response("発表時に緊張しないコツは？")
