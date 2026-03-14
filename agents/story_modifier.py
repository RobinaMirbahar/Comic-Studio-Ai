from .agent_base import create_agent

instruction = """
You are a story editor. You will receive an existing comic story (in JSON format) and a user request for modification.
Modify the story according to the request while preserving the overall structure (title, characters list, plot list).
Return the modified story in the exact same JSON format.

Example modification: "Make the main character more brave" → adjust character description and perhaps dialogue in plot.
"""

modifier = create_agent(
    name="story_modifier",
    description="Modifies a story based on user feedback.",
    instruction=instruction,
)
