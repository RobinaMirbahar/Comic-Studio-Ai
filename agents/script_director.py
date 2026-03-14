from pydantic import BaseModel, Field
from typing import Literal, Optional
from .agent_base import create_agent

class ScriptFeedback(BaseModel):
    status: Literal["pass", "fail"] = Field(description="Whether the script meets quality standards.")
    feedback: str = Field(description="If fail, detailed explanation of what's missing.")
    revised_script: Optional[dict] = Field(default=None, description="If possible, an improved version of the story in the same format.")

instruction = """
You are a Script Director in a comic studio. Your job is to evaluate story scripts and ensure they are ready for the storyboard artist.

**Criteria:**
- All characters must have unique names and clear descriptions (no generic names like "Friend").
- Each plot point must be a specific event (not generic like "Beginning").
- The story should be engaging and coherent.

If the script passes all criteria, return status="pass".
If it fails, return status="fail" with specific feedback and, if you can, provide a revised_script that fixes the issues.
"""

script_director = create_agent(
    name="script_director",
    description="Evaluates story quality and provides feedback.",
    instruction=instruction,
    output_schema=ScriptFeedback,
)
