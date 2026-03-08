import os
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import time
import random
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class PanelGeneratorAgent:
    """Generates comic images based on user prompt"""
    
    def __init__(self):
        self.model = genai.GenerativeModel("models/nano-banana-pro-preview")
        self.name = "panel_generator"
        self.character_processor = None
        print("✅ Panel Generator Ready")
    
    def set_character_processor(self, processor):
        self.character_processor = processor
    
    def generate_pages(self, story, language="en", style="manga", character_ids=None, prompt="", output_dir="static/comics"):
        """Generate 4 comic pages based on the user's prompt"""
        
        print(f"\n{'='*50}")
        print(f"🎨 GENERATING COMIC FOR PROMPT: '{prompt}'")
        print(f"🎨 STYLE: {style}")
        print(f"{'='*50}\n")
        
        os.makedirs(output_dir, exist_ok=True)
        pages = []
        
        # Get story elements
        title = story.get('title', 'Adventure')
        characters = story.get('characters', ['Hero', 'Friend'])
        plot = story.get('plot', ['Scene 1', 'Scene 2', 'Scene 3', 'Scene 4'])
        
        main_character = characters[0] if characters else "Hero"
        
        # Style mapping
        style_desc = {
            "sketch": "pencil sketch, black and white, rough lines, hand-drawn",
            "manga": "japanese manga, black and white, screentones, dynamic",
            "western": "american comic book, bold colors, superhero style",
            "anime": "japanese anime, vibrant colors, cel-shaded",
            "watercolor": "watercolor painting, soft colors, artistic",
            "vintage": "vintage 1950s comic, muted colors, halftone dots"
        }
        
        style_text = style_desc.get(style, style_desc["manga"])
        
        # Generate 4 panels based on the user's prompt
        for i in range(4):
            # Create scene descriptions based on the prompt
            scenes = [
                f"Scene 1 - Beginning: {prompt} - The adventure starts",
                f"Scene 2 - Journey: {prompt} - The journey continues",
                f"Scene 3 - Challenge: {prompt} - An exciting challenge",
                f"Scene 4 - Conclusion: {prompt} - The grand finale"
            ]
            
            # Add bubble instructions
            bubbles = [
                "Include a speech bubble with exciting dialogue",
                "Include a thought bubble showing inner thoughts",
                "Include an exclamation bubble like 'WOW!' or 'AMAZING!'",
                "Include a sound effect bubble like 'BOOM!' or 'THE END'"
            ]
            
            full_prompt = f"""
            Create a comic panel in {style_text} style.
            
            SCENE: {scenes[i]}
            
            CHARACTERS: {main_character} is the main character. Other characters: {', '.join(characters[1:])}
            
            REQUIREMENTS:
            - This is Panel {i+1} of 4
            - MUST show {main_character} clearly
            - MUST include a comic bubble: {bubbles[i]}
            - MUST be in {style_text} style
            - Make it fun and engaging
            
            IMPORTANT: This is NOT a camel unless the prompt says "camel". The prompt is: "{prompt}"
            """
            
            print(f"📦 Generating panel {i+1} for: '{prompt[:30]}...'")
            
            try:
                response = self.model.generate_content(
                    full_prompt,
                    generation_config={
                        "temperature": 0.9,
                        "max_output_tokens": 4096,
                    }
                )
                
                if response.parts and hasattr(response.parts[0], 'inline_data'):
                    image_data = response.parts[0].inline_data.data
                    image = Image.open(BytesIO(image_data))
                    
                    filename = f"page_{i+1}.png"
                    filepath = os.path.join(output_dir, filename)
                    image.save(filepath, quality=95)
                    
                    pages.append(f"/static/comics/{filename}")
                    print(f"✅ Panel {i+1} generated for: {prompt}")
                else:
                    print(f"⚠️ No image data for panel {i+1}")
                    pages.append(self._create_fallback(output_dir, i+1, prompt, style, main_character))
                
                time.sleep(2)
                
            except Exception as e:
                print(f"⚠️ Error for panel {i+1}: {e}")
                pages.append(self._create_fallback(output_dir, i+1, prompt, style, main_character))
        
        print(f"\n✅ Generated {len(pages)} panels for: {prompt}")
        return pages
    
    def _create_fallback(self, output_dir, page_num, prompt, style, character):
        """Create a fallback image showing the actual prompt"""
        try:
            # Create image
            img = Image.new('RGB', (512, 512), color=(255, 255, 255))
            draw = ImageDraw.Draw(img)
            
            # Draw border
            draw.rectangle([10, 10, 502, 502], outline=(0, 0, 0), width=3)
            
            # Draw title
            draw.text((20, 30), f"PAGE {page_num}", fill=(0, 0, 0))
            draw.text((20, 70), f"PROMPT: {prompt}", fill=(200, 0, 0))
            draw.text((20, 110), f"STYLE: {style}", fill=(0, 0, 200))
            draw.text((20, 150), f"CHARACTER: {character}", fill=(0, 150, 0))
            
            # Draw based on prompt (but NOT camel unless specified)
            if "mouse" in prompt.lower():
                # Draw a mouse
                draw.ellipse((200, 200, 300, 280), outline=(0, 0, 0), width=2)
                draw.ellipse((280, 180, 320, 220), outline=(0, 0, 0), width=2)
                draw.ellipse((295, 190, 305, 200), fill=(0, 0, 0))
                draw.line((300, 210, 320, 220), fill=(0, 0, 0), width=1)
                
                # Add bubble
                draw.ellipse((350, 120, 450, 170), outline=(0, 0, 0), width=2)
                draw.text((370, 135), "Squeak!", fill=(0, 0, 0))
                
            elif "road" in prompt.lower():
                # Draw a road scene
                draw.rectangle((100, 300, 400, 350), fill=(100, 100, 100))
                draw.line((100, 325, 400, 325), fill=(255, 255, 0), width=3)
                
                # Draw a car
                draw.rectangle((200, 220, 300, 280), outline=(0, 0, 255), width=2)
                draw.ellipse((220, 260, 240, 280), fill=(0, 0, 0))
                draw.ellipse((260, 260, 280, 280), fill=(0, 0, 0))
                
                # Add bubble
                draw.ellipse((320, 150, 420, 200), outline=(255, 0, 0), width=2)
                draw.text((340, 165), "Vroom!", fill=(255, 0, 0))
                
            elif "cat" in prompt.lower():
                # Draw a cat
                draw.ellipse((200, 200, 300, 280), outline=(0, 0, 0), width=2)
                draw.ellipse((220, 180, 260, 220), outline=(0, 0, 0), width=2)
                draw.ellipse((280, 180, 320, 220), outline=(0, 0, 0), width=2)
                draw.line((240, 160, 230, 140), fill=(0, 0, 0), width=2)
                draw.line((300, 160, 310, 140), fill=(0, 0, 0), width=2)
                
                # Add bubble
                draw.ellipse((350, 120, 450, 170), outline=(0, 0, 0), width=2)
                draw.text((370, 135), "Meow!", fill=(0, 0, 0))
                
            elif "dog" in prompt.lower():
                # Draw a dog
                draw.ellipse((200, 200, 300, 280), outline=(0, 0, 0), width=2)
                draw.ellipse((280, 180, 330, 230), outline=(0, 0, 0), width=2)
                draw.ellipse((300, 190, 310, 200), fill=(0, 0, 0))
                draw.ellipse((170, 190, 200, 220), outline=(0, 0, 0), width=2)
                
                # Add bubble
                draw.ellipse((350, 120, 450, 170), outline=(0, 0, 0), width=2)
                draw.text((370, 135), "Woof!", fill=(0, 0, 0))
                
            else:
                # Draw a generic character
                draw.ellipse((200, 150, 300, 250), outline=(0, 0, 0), width=2)
                draw.line((250, 250, 250, 350), fill=(0, 0, 0), width=2)
                draw.line((250, 350, 200, 400), fill=(0, 0, 0), width=2)
                draw.line((250, 350, 300, 400), fill=(0, 0, 0), width=2)
                draw.line((250, 280, 200, 300), fill=(0, 0, 0), width=2)
                draw.line((250, 280, 300, 300), fill=(0, 0, 0), width=2)
                
                # Add thought bubble
                draw.ellipse((320, 80, 420, 130), outline=(0, 0, 0), width=2)
                draw.ellipse((410, 120, 430, 140), outline=(0, 0, 0), width=2)
                draw.ellipse((420, 130, 440, 150), outline=(0, 0, 0), width=2)
                draw.text((340, 95), f"{prompt[:20]}...", fill=(0, 0, 0))
            
            # Save image
            filename = f"page_{page_num}.png"
            filepath = os.path.join(output_dir, filename)
            img.save(filepath)
            
            print(f"📸 Created fallback for panel {page_num} with prompt: {prompt}")
            return f"/static/comics/{filename}"
            
        except Exception as e:
            print(f"❌ Fallback failed: {e}")
            return ""

    # Add this method to help debug
    def debug_generate(self, story, language="en", style="manga", character_ids=None, prompt="", output_dir="static/comics"):
        print(f"\n🔍 DEBUG - PanelGenerator received:")
        print(f"   prompt: '{prompt}'")
        print(f"   style: '{style}'")
        print(f"   story title: '{story.get('title', 'N/A')}'")
        return self.generate_pages(story, language, style, character_ids, prompt, output_dir)
