from .agent_base import create_agent

instruction = """
You are a dialogue expert. For each panel description, write natural dialogue or thoughts for the characters.

Return a JSON array of 4 objects, each with fields: panel_number, dialogues (list of {character, text, bubble_type}).
Bubble types: speech, thought, shout, whisper.
"""

dialogue_doctor = create_agent(
    name="dialogue_doctor",
    description="Adds dialogue bubbles to comic panels.",
    instruction=instruction,
)
