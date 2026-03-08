import os
from PIL import Image, ImageDraw, ImageFont
import os

class BubbleDrawer:
    """Simple bubble drawer for comics"""
    
    def __init__(self):
        print("✅ Bubble Drawer Ready")
    
    def add_bubble(self, image_url, text, bubble_type="speech", emotion="neutral", position="bottom"):
        """Add a bubble to an image"""
        try:
            # Extract filename from URL
            if image_url.startswith('/static/') or image_url.startswith('/comics/'):
                filename = image_url.split('/')[-1].split('?')[0]  # Remove query params
                image_path = os.path.join('static/comics', filename)
            else:
                image_path = image_url
            
            print(f"📸 Loading image from: {image_path}")
            
            # Check if file exists
            if not os.path.exists(image_path):
                print(f"❌ Image not found: {image_path}")
                return image_url
            
            # Open the image
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)
            width, height = img.size
            
            # Load font
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
            except:
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 30)
                except:
                    font = ImageFont.load_default()
            
            # Wrap text
            words = text.split()
            lines = []
            current_line = []
            for word in words:
                current_line.append(word)
                # Check line width
                line_text = ' '.join(current_line)
                bbox = draw.textbbox((0, 0), line_text, font=font)
                if bbox[2] - bbox[0] > 300:  # Max width 300px
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))
            
            if not lines:
                lines = [text]
            
            # Calculate bubble size
            line_height = 40
            text_height = len(lines) * line_height
            max_line_width = 0
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                line_width = bbox[2] - bbox[0]
                max_line_width = max(max_line_width, line_width)
            
            padding = 30
            bubble_width = max_line_width + padding * 2
            bubble_height = text_height + padding * 2
            
            # Determine position
            margin = 30
            if position == "top":
                x = (width - bubble_width) // 2
                y = margin
            elif position == "bottom":
                x = (width - bubble_width) // 2
                y = height - bubble_height - margin
            elif position == "left":
                x = margin
                y = (height - bubble_height) // 2
            elif position == "right":
                x = width - bubble_width - margin
                y = (height - bubble_height) // 2
            else:  # auto
                x = (width - bubble_width) // 2
                y = height - bubble_height - margin
            
            # Draw bubble based on type
            if bubble_type == "speech":
                self._draw_speech_bubble(draw, x, y, bubble_width, bubble_height)
            elif bubble_type == "thought":
                self._draw_thought_bubble(draw, x, y, bubble_width, bubble_height)
            elif bubble_type == "shout":
                self._draw_shout_bubble(draw, x, y, bubble_width, bubble_height)
            elif bubble_type == "whisper":
                self._draw_whisper_bubble(draw, x, y, bubble_width, bubble_height)
            elif bubble_type == "narration":
                self._draw_narration_box(draw, x, y, bubble_width, bubble_height)
            elif bubble_type == "sfx":
                self._draw_sfx(draw, x, y, text, width, height, font)
                return self._save_image(img, image_path)
            
            # Draw text
            y_text = y + padding
            for line in lines:
                draw.text((x + padding, y_text), line, fill="black", font=font)
                y_text += line_height
            
            # Add emotion emoji if not neutral
            if emotion != "neutral":
                emoji_map = {
                    "happy": "😊",
                    "sad": "😢",
                    "angry": "😠",
                    "excited": "🤩",
                    "scared": "😨"
                }
                if emotion in emoji_map:
                    draw.text((x + bubble_width - 50, y + 10), emoji_map[emotion], fill="black", font=font)
            
            return self._save_image(img, image_path)
            
        except Exception as e:
            print(f"❌ Bubble error: {e}")
            return image_url
    
    def _draw_speech_bubble(self, draw, x, y, w, h):
        """Draw a speech bubble"""
        # Main bubble
        draw.ellipse([x, y, x + w, y + h], outline="black", width=3, fill="white")
        # Tail
        draw.polygon([(x + w//2, y + h), (x + w//2 + 20, y + h + 30), (x + w//2 - 20, y + h + 30)], 
                     outline="black", fill="white")
    
    def _draw_thought_bubble(self, draw, x, y, w, h):
        """Draw a thought bubble"""
        # Main cloud
        draw.ellipse([x, y, x + w, y + h], outline="black", width=2, fill="#f0f0f0")
        # Thought circles
        draw.ellipse([x + w//2 - 20, y + h, x + w//2, y + h + 20], outline="black", width=1, fill="#f0f0f0")
        draw.ellipse([x + w//2 - 5, y + h + 15, x + w//2 + 15, y + h + 35], outline="black", width=1, fill="#f0f0f0")
    
    def _draw_shout_bubble(self, draw, x, y, w, h):
        """Draw a shout/exclamation bubble"""
        # Main bubble with jagged edges
        draw.rectangle([x, y, x + w, y + h], outline="red", width=4, fill="#ffd700")
        # Jagged edges
        for i in range(0, w, 30):
            draw.line([x + i, y, x + i + 15, y - 10], fill="red", width=2)
    
    def _draw_whisper_bubble(self, draw, x, y, w, h):
        """Draw a whisper bubble (dotted)"""
        # Dotted rectangle
        for i in range(0, w, 10):
            draw.point((x + i, y), fill="gray")
            draw.point((x + i, y + h), fill="gray")
        for i in range(0, h, 10):
            draw.point((x, y + i), fill="gray")
            draw.point((x + w, y + i), fill="gray")
        # Fill
        draw.rectangle([x+1, y+1, x + w-1, y + h-1], outline=None, fill="#e0e0e0")
    
    def _draw_narration_box(self, draw, x, y, w, h):
        """Draw a narration box"""
        draw.rectangle([x, y, x + w, y + h], outline="brown", width=3, fill="#ffffe0")
    
    def _draw_sfx(self, draw, x, y, text, width, height, font):
        """Draw sound effect text"""
        try:
            bold_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        except:
            bold_font = font
        
        text = text.upper()
        bbox = draw.textbbox((0, 0), text, font=bold_font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        x = (width - text_w) // 2
        y = height // 3
        
        # Draw shadow
        draw.text((x+3, y+3), text, fill="gray", font=bold_font)
        # Draw main text
        draw.text((x, y), text, fill="red", font=bold_font)
    
    def _save_image(self, img, original_path):
        """Save the image with bubble"""
        try:
            filename = os.path.basename(original_path)
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_bubble{ext}"
            new_path = os.path.join('static/comics', new_filename)
            img.save(new_path)
            print(f"💾 Saved bubble image to: {new_path}")
            return f"/static/comics/{new_filename}"
        except Exception as e:
            print(f"❌ Save error: {e}")
            return original_path
