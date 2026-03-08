import os
import random
import google.generativeai as genai
from dotenv import load_dotenv
import re

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class StoryGeneratorAgent:
    """Creates unique stories using the FULL prompt"""
    
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.name = "story_generator"
        print("✅ Advanced Story Generator Ready")
    
    def generate(self, topic):
        """Generate a story using Gemini AI for real variety"""
        
        # Use Gemini to generate a truly unique story
        prompt = f"""
        Create a short 4-panel comic story based on this idea: "{topic}"
        
        Return a JSON object with:
        - title: A creative title (use the FULL idea, don't truncate)
        - characters: 2 character names with brief descriptions
        - plot: 4 short sentences for each panel
        
        Make it fun and creative! Use the ENTIRE prompt to inspire the story.
        
        Example format:
        {{
            "title": "The Full Story Title",
            "characters": ["Name1 - description", "Name2 - description"],
            "plot": ["Panel 1 action", "Panel 2 action", "Panel 3 action", "Panel 4 action"]
        }}
        
        Return ONLY the JSON, no other text.
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            text = response.text
            # Find JSON between curly braces
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                import json
                story = json.loads(json_match.group())
                
                # Ensure we have all required fields
                if 'title' not in story:
                    story['title'] = topic[:30] + "..."
                if 'characters' not in story:
                    story['characters'] = ["Hero", "Friend"]
                if 'plot' not in story or len(story['plot']) < 4:
                    story['plot'] = [
                        f"{story['characters'][0] if 'characters' in story else 'Hero'} begins",
                        "A challenge appears",
                        "Friends work together",
                        "Happy ending"
                    ]
                
                return story
            else:
                # Fallback if JSON parsing fails
                return self._create_fallback_story(topic)
                
        except Exception as e:
            print(f"⚠️ Gemini story generation failed: {e}")
            return self._create_fallback_story(topic)
    
    def _create_fallback_story(self, topic):
        """Create a story based on keywords if AI fails"""
        topic_lower = topic.lower()
        
        # Cat story
        if 'cat' in topic_lower:
            return {
                "title": topic[:40],
                "characters": ["Whiskers - a curious cat", "Shadow - a mysterious alley cat"],
                "plot": [
                    f"{topic} - Whiskers explores an old garage",
                    "She finds a magical yarn ball that glows",
                    "Shadow the alley cat appears and warns her",
                    "Together they discover a hidden cat kingdom"
                ]
            }
        # Robot story
        elif 'robot' in topic_lower:
            return {
                "title": topic[:40],
                "characters": ["Circuit - a friendly robot", "Byte - a helpful AI"],
                "plot": [
                    f"{topic} - Circuit wakes up on Mars",
                    "Byte helps him find power cells",
                    "They discover ancient alien technology",
                    "They befriend the Martians and celebrate"
                ]
            }
        # Space story
        elif any(word in topic_lower for word in ['space', 'mars', 'moon', 'alien']):
            return {
                "title": topic[:40],
                "characters": ["Captain Nova - brave astronaut", "Zork - curious alien"],
                "plot": [
                    f"{topic} - Captain Nova lands on a new planet",
                    "She meets Zork the alien",
                    "They explore ancient ruins together",
                    "They become best friends across galaxies"
                ]
            }
        # Default story
        else:
            return {
                "title": topic[:40],
                "characters": ["Alex - the adventurer", "Jamie - the guide"],
                "plot": [
                    f"{topic} - The adventure begins",
                    "A mysterious discovery is made",
                    "A new friend appears to help",
                    "Together they succeed and celebrate"
                ]
            }
