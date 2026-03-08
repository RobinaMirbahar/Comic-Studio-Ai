import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class ScriptDirectorAgent:
    """Converts story to comic script with panel descriptions"""
    
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.name = "script_director"
        print("✅ Script Director Ready")
    
    def create_script(self, story, panels=4, style="manga"):
        """Convert story to detailed comic script"""
        
        title = story.get('title', 'Comic')
        characters = story.get('characters', ['Hero', 'Friend'])
        plot = story.get('plot', ['Scene 1', 'Scene 2', 'Scene 3', 'Scene 4'])
        
        prompt = f"""
        Create a detailed comic script for a {style} style comic.
        
        STORY TITLE: {title}
        CHARACTERS: {', '.join(characters)}
        PLOT: {' '.join(plot)}
        
        For each of the {panels} panels, provide:
        - Panel number
        - Camera angle (close-up, wide shot, medium, low angle, bird's eye)
        - Character expressions and poses
        - Background description
        - Lighting mood
        - Dialogue (if any)
        
        Format as JSON.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except:
            return {"panels": []}
