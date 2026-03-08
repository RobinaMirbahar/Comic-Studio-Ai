import os
import uuid
import shutil
from PIL import Image
import json

class CharacterProcessor:
    """Processes uploaded characters for use in comic generation"""
    
    def __init__(self):
        self.upload_dir = "static/uploads"
        self.characters_file = "static/characters.json"
        os.makedirs(self.upload_dir, exist_ok=True)
        self.characters = self._load_characters()
        print("✅ Character Processor Ready with AI integration")
    
    def _load_characters(self):
        """Load saved characters from JSON"""
        if os.path.exists(self.characters_file):
            try:
                with open(self.characters_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_characters(self):
        """Save characters to JSON"""
        with open(self.characters_file, 'w') as f:
            json.dump(self.characters, f)
    
    def save_character(self, image_data, filename):
        """Save an uploaded character image"""
        try:
            # Generate unique ID
            char_id = str(uuid.uuid4())[:8]
            timestamp = int(time.time())
            
            # Get file extension
            ext = os.path.splitext(filename)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
                ext = '.jpg'  # Default
            
            # Save original image
            new_filename = f"char_{char_id}_{timestamp}{ext}"
            filepath = os.path.join(self.upload_dir, new_filename)
            
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            # Create thumbnail
            thumb_filename = f"thumb_{char_id}_{timestamp}.jpg"
            thumb_path = os.path.join(self.upload_dir, thumb_filename)
            self._create_thumbnail(filepath, thumb_path)
            
            # Save character info
            character = {
                "id": char_id,
                "filename": new_filename,
                "thumbnail": thumb_filename,
                "original_name": filename,
                "uploaded_at": timestamp,
                "url": f"/static/uploads/{new_filename}",
                "thumb_url": f"/static/uploads/{thumb_filename}"
            }
            
            self.characters.append(character)
            self._save_characters()
            
            print(f"✅ Character saved: {filename} -> {new_filename}")
            
            return {
                "success": True,
                "id": char_id,
                "url": character["url"],
                "thumb_url": character["thumb_url"]
            }
            
        except Exception as e:
            print(f"❌ Error saving character: {e}")
            return {"success": False, "error": str(e)}
    
    def _create_thumbnail(self, image_path, thumb_path, size=(100, 100)):
        """Create a thumbnail for the character"""
        try:
            img = Image.open(image_path)
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(thumb_path, "JPEG")
        except Exception as e:
            print(f"⚠️ Thumbnail error: {e}")
    
    def get_all_characters(self):
        """Return all saved characters"""
        return self.characters
    
    def get_character(self, char_id):
        """Get a specific character by ID"""
        for char in self.characters:
            if char["id"] == char_id:
                return char
        return None
    
    def delete_character(self, char_id):
        """Delete a character by ID"""
        for i, char in enumerate(self.characters):
            if char["id"] == char_id:
                # Delete files
                try:
                    os.remove(os.path.join(self.upload_dir, char["filename"]))
                    os.remove(os.path.join(self.upload_dir, char["thumbnail"]))
                except:
                    pass
                # Remove from list
                self.characters.pop(i)
                self._save_characters()
                return True
        return False
    
    def get_character_image(self, char_id):
        """Get the image path for a character (for AI generation)"""
        char = self.get_character(char_id)
        if char:
            return os.path.join(self.upload_dir, char["filename"])
        return None
