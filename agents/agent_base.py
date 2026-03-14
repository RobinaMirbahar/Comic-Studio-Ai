import os
from google.adk.agents import Agent
from google.adk.models import GeminiModel

# Model name (can be changed)
MODEL_NAME = "gemini-2.0-flash"

def create_agent(name, description, instruction, tools=None, output_schema=None):
    """Factory to create a standard agent with Gemini."""
    return Agent(
        name=name,
        model=GeminiModel(model=MODEL_NAME),
        description=description,
        instruction=instruction,
        tools=tools or [],
        output_schema=output_schema,
    )
