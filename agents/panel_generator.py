from .agent_base import create_agent

instruction = """
You are a comic panel director. Take the approved story and break it into 4 visual panels.

For each panel, describe:
- What happens visually
- Character positions and expressions
- Background elements

Return a JSON array of 4 objects, each with fields: panel_number, description, characters_present, suggested_art_style.
"""

panel_generator = create_agent(
    name="panel_generator",
    description="Creates visual panel descriptions from a story.",
    instruction=instruction,
)
