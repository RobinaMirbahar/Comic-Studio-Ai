import os
import json
import random
from PIL import Image, ImageDraw, ImageFont
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class DialogueAgent:
    """Complete dialogue and lettering system for comics"""
    
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.bubble_styles = {
            "speech": {"color": "white", "outline": "black", "tail": True, "shape": "rounded"},
            "thought": {"color": "#f0f0f0", "outline": "black", "tail": False, "shape": "cloud"},
            "shout": {"color": "#ffd700", "outline": "red", "tail": True, "shape": "jagged"},
            "whisper": {"color": "#e0e0e0", "outline": "gray", "tail": True, "shape": "dotted"},
            "narration": {"color": "#ffffe0", "outline": "brown", "tail": False, "shape": "rectangle"},
            "sfx": {"color": "transparent", "outline": "none", "tail": False, "shape": "text-only"}
        }
        print("✅ Dialogue Agent Ready")
    
    # ==================== AI DIALOGUE GENERATION ====================
    def generate_dialogue(self, scene_description, characters, panel_number):
        """AI suggests dialogue based on scene"""
        prompt = f"""
        Generate comic dialogue for Panel {panel_number}.
        
        Scene: {scene_description}
        Characters: {', '.join(characters)}
        
        Create natural dialogue that:
        - Advances the story
        - Shows character personalities
        - Fits the mood of the scene
        
        Return JSON with:
        {{
            "lines": [
                {{"character": "Name", "text": "dialogue line", "emotion": "happy/sad/angry"}}
            ],
            "sound_effects": ["BOOM!", "CRASH"] (optional)
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            print(f"Dialogue generation error: {e}")
            return {
                "lines": [
                    {"character": characters[0] if characters else "Hero", 
                     "text": "...", 
                     "emotion": "neutral"}
                ],
                "sound_effects": []
            }
    
    # ==================== BUBBLE DRAWING FUNCTIONS ====================
    def draw_speech_bubble(self, draw, x, y, width, height, text, style="speech"):
        """Draw different types of speech bubbles"""
        
        styles = {
            "speech": self._draw_rounded_bubble,
            "thought": self._draw_thought_bubble,
            "shout": self._draw_jagged_bubble,
            "whisper": self._draw_dotted_bubble,
            "narration": self._draw_narration_box,
            "sfx": self._draw_sound_effect
        }
        
        style_func = styles.get(style, self._draw_rounded_bubble)
        return style_func(draw, x, y, width, height, text)
    
    def _draw_rounded_bubble(self, draw, x, y, width, height, text):
        """Standard speech bubble"""
        # Draw bubble
        draw.rounded_rectangle([x, y, x+width, y+height], radius=15, 
                              fill="white", outline="black", width=2)
        # Draw tail
        tail_points = [(x+30, y+height), (x+50, y+height+20), (x+70, y+height)]
        draw.polygon(tail_points, fill="white", outline="black")
        # Add text
        draw.text((x+15, y+15), text, fill="black")
        return (x+width, y+height)
    
    def _draw_thought_bubble(self, draw, x, y, width, height, text):
        """Cloud-like thought bubble"""
        # Main bubble
        draw.ellipse([x, y, x+width, y+height], fill="#f0f0f0", outline="black", width=2)
        # Smaller bubbles
        draw.ellipse([x-15, y+20, x+15, y+50], fill="#f0f0f0", outline="black", width=1)
        draw.ellipse([x-25, y+40, x-5, y+60], fill="#f0f0f0", outline="black", width=1)
        # Add text
        draw.text((x+20, y+20), text, fill="black")
        return (x+width, y+height)
    
    def _draw_jagged_bubble(self, draw, x, y, width, height, text):
        """Shout bubble with jagged edges"""
        # Draw jagged rectangle
        points = []
        for i in range(0, width+1, 10):
            points.append((x+i, y + (5 if i%20==0 else -5)))
        for i in range(0, height+1, 10):
            points.append((x+width, y+i + (5 if i%20==0 else -5)))
        # ... (simplified for this example)
        draw.rectangle([x, y, x+width, y+height], fill="#ffd700", outline="red", width=3)
        draw.text((x+15, y+15), text.upper(), fill="red")
        return (x+width, y+height)
    
    def _draw_dotted_bubble(self, draw, x, y, width, height, text):
        """Whisper bubble with dotted outline"""
        for i in range(0, width, 5):
            draw.point((x+i, y), fill="gray")
            draw.point((x+i, y+height), fill="gray")
        for i in range(0, height, 5):
            draw.point((x, y+i), fill="gray")
            draw.point((x+width, y+i), fill="gray")
        draw.text((x+15, y+15), text, fill="gray")
        return (x+width, y+height)
    
    def _draw_narration_box(self, draw, x, y, width, height, text):
        """Narration/ caption box"""
        draw.rectangle([x, y, x+width, y+height], fill="#ffffe0", outline="brown", width=2)
        draw.text((x+10, y+10), text, fill="brown")
        return (x+width, y+height)
    
    def _draw_sound_effect(self, draw, x, y, text):
        """Sound effect (SFX)"""
        draw.text((x, y), text.upper(), fill="red", font=None)
        return (x+100, y+30)
    
    # ==================== AUTO-LETTERING ====================
    def auto_letter_page(self, image_path, scene_text, characters, style="manga"):
        """Automatically add bubbles to a page"""
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # Generate dialogue
        dialogue = self.generate_dialogue(scene_text, characters, 1)
        
        # Position bubbles based on style
        positions = {
            "manga": [(100, 50), (400, 300), (100, 500)],
            "western": [(150, 80), (450, 350), (150, 550)],
            "anime": [(80, 40), (380, 280), (120, 480)]
        }
        
        pos_list = positions.get(style, positions["manga"])
        
        # Draw bubbles for each line
        for i, line in enumerate(dialogue.get("lines", [])):
            if i < len(pos_list):
                x, y = pos_list[i]
                emotion = line.get("emotion", "neutral")
                bubble_style = "shout" if emotion == "angry" else "speech"
                self.draw_speech_bubble(draw, x, y, 200, 60, line["text"], bubble_style)
        
        # Draw sound effects
        sfx = dialogue.get("sound_effects", [])
        for i, sound in enumerate(sfx):
            self._draw_sound_effect(draw, 500 + i*100, 600, sound)
        
        return img
    
    # ==================== MANUAL BUBBLE EDITING ====================
    def add_manual_bubble(self, image_path, text, bubble_type, x, y):
        """Manually add a bubble at specific coordinates"""
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        self.draw_speech_bubble(draw, x, y, 200, 60, text, bubble_type)
        return img
    
    # ==================== BUBBLE STYLE PRESETS ====================
    def get_bubble_presets(self):
        """Return available bubble styles"""
        return list(self.bubble_styles.keys())
    
    def preview_bubble(self, style):
        """Preview a bubble style"""
        return self.bubble_styles.get(style, self.bubble_styles["speech"])
