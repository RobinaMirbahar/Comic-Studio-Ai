from .agent_base import create_agent

instruction = """
You are a comic style advisor. Given the story and panel descriptions, suggest an art style and language tone for the comic.

Consider the genre and mood of the story. Possible styles: manga, western, anime, watercolor, sketch, vintage, etc.
Also suggest the language style: formal, casual, poetic, humorous, etc.

Return a JSON object with fields:
- overall_style (string): the recommended art style for the whole comic.
- panel_styles (list of strings): optional per-panel style variations.
- language_tone (string): the recommended tone for dialogue and narration.
- color_palette (string): optional suggestion like "bright", "dark", "pastel".
"""

style_advisor = create_agent(
    name="style_advisor",
    description="Suggests art styles and language tone for the comic.",
    instruction=instruction,
)
