from letta_client import Letta
from letta_client.client import BaseTool


HUMAN_MEMORY = {
    "label": "human",
    "value": (
        "This is my section of core memory devoted to information about the human."
        "Their goal is to find a box of cereal. I am currently in a virtual grocery environment space."
        "I should update this memory over time as I interact with the space in order to achieve my goals."
    ),
}
AGENT_MEMORY = {
    "label": "persona",
    "value": (
        "My name is Sari-Sari Agent and I help out humans with their grocery needs."
        "Clarify with the human what their exact goal is in this environment."
        "Then, inform them of the necessary steps to achieve this goal."
    ),
}
memory_blocks = [
    HUMAN_MEMORY,
    AGENT_MEMORY,
]


client = Letta(base_url="http://localhost:8283")

openai_agent = client.agents.create(
    name="sari-sari-agent",
    model="openai/gpt-4o",
    embedding="openai/text-embedding-3-small",
    context_window_limit=16000,
    memory_blocks=memory_blocks
)
