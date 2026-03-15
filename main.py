import os
import json
import re
import base64
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import google.generativeai as genai
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib.utils import ImageReader
from io import BytesIO
from PIL import Image as PILImage

<<<<<<< HEAD

=======
# Configure Gemini – API key must be set in environment variable
>>>>>>> b5a680c18f350d61d856dc464552880242d2aeab
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")
genai.configure(api_key=api_key)
<<<<<<< HEAD
print("Using API key starting with:", api_key[:10] if api_key else "None")


=======
>>>>>>> b5a680c18f350d61d856dc464552880242d2aeab

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def call_gemini(prompt, model="gemini-2.0-flash"):
    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt)
    return response.text

def call_gemini_with_image(prompt, image_data):
    """Send prompt and image (base64) to Gemini."""
    model = genai.GenerativeModel('gemini-2.0-flash')
    # Convert base64 to bytes
    image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_bytes
        }
    ]
    response = model.generate_content([prompt, image_parts[0]])
    return response.text

def generate_image(prompt):
    """Generate an image using Nano Banana 2 (gemini-3.1-flash-image-preview)"""
    try:
        model = genai.GenerativeModel('gemini-3.1-flash-image-preview')
        response = model.generate_content(prompt)
        for part in response.parts:
            if part.inline_data and part.inline_data.mime_type.startswith('image/'):
                return base64.b64encode(part.inline_data.data).decode('utf-8')
        print("No image data in response")
        return None
    except Exception as e:
        print(f"Image generation failed: {e}")
        return None

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate-story")
async def generate_story(request: dict):
    topic = request.get("topic", "")
    language = request.get("language", "English")
    panels = request.get("panels", 4)
    prompt = f"""
    You are a comic story researcher. Create a {panels}-panel comic story about: {topic}
    The story MUST be written in {language}. All character names, descriptions, and plot must be in {language}.
    Return ONLY a JSON object with fields:
    - title (string, in {language})
    - characters (list of strings, each string MUST be in the format "Name - Description" in {language})
    - plot (list of {panels} strings, each describing a panel's action/dialogue, in {language})
    """
    text = call_gemini(prompt)
    match = re.search(r'\{.*\}', text, re.DOTALL)
    story = json.loads(match.group()) if match else {"title": "Story", "characters": [], "plot": []}
    return JSONResponse(content={"story": story})

@app.post("/generate-story-with-image")
async def generate_story_with_image(request: dict):
    topic = request.get("topic", "")
    language = request.get("language", "English")
    panels = request.get("panels", 4)
    image_data = request.get("image")  # base64 image (may include data:image prefix)

    prompt = f"""
    You are a comic story researcher. Create a {panels}-panel comic story about: {topic}
    The MAIN CHARACTER should look exactly like the person/character in the provided image.
    Describe that character in detail in the 'characters' list, and make them the central figure.
    The story MUST be written in {language}. All character names, descriptions, and plot must be in {language}.
    Return ONLY a JSON object with fields:
    - title (string, in {language})
    - characters (list of strings, each string MUST be in the format "Name - Description" in {language})
    - plot (list of {panels} strings, each describing a panel's action/dialogue, in {language})
    """
    try:
        text = call_gemini_with_image(prompt, image_data)
        match = re.search(r'\{.*\}', text, re.DOTALL)
        story = json.loads(match.group()) if match else {"title": "Story", "characters": [], "plot": []}
        return JSONResponse(content={"story": story})
    except Exception as e:
        print(f"Error with image story: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/refine-story")
async def refine_story(request: dict):
    story = request.get("story")
    modification = request.get("modification")
    language = request.get("language", "English")
    prompt = f"""
    You are a helpful story editor. Modify the following story according to the user's request.
    Story: {json.dumps(story)}
    User request: {modification}
    IMPORTANT: PRESERVE ALL EXISTING CHARACTERS. Do NOT remove or replace any existing characters unless the user explicitly asks to remove one.
    If the user asks to add a new character, add it to the characters list while keeping all previous characters.
    The characters list must remain a list of strings in the format "Name - Description".
    The plot must remain a list of strings (same length as original).
    All text must be in {language}.
    Return the modified story in the exact same JSON format (title, characters list, plot list).
    """
    text = call_gemini(prompt)
    match = re.search(r'\{.*\}', text, re.DOTALL)
    modified = json.loads(match.group()) if match else story
    return JSONResponse(content={"story": modified})

@app.post("/generate-panels")
async def generate_panels(request: dict):
    story = request.get("story")
    user_style = request.get("style", {})
    language = request.get("language", "English")
    panels_count = len(story.get("plot", []))
    style_instruction = ""
    if user_style.get("overall_style"):
        style_instruction += f" Use {user_style['overall_style']} art style."
    if user_style.get("language_tone"):
        style_instruction += f" Use {user_style['language_tone']} language tone."
    if user_style.get("color_palette"):
        style_instruction += f" Color palette: {user_style['color_palette']}."

    panel_prompt = f"""
    You are a comic panel director. Based on this story, create {panels_count} visual panel descriptions.
    Story: {json.dumps(story)}
    {style_instruction}
    All descriptions MUST be written in {language}.
    Return ONLY a JSON array of {panels_count} objects with fields: panel_number (int), description (string), characters_present (list of strings), suggested_art_style (string).
    """
    panel_text = call_gemini(panel_prompt, model="nano-banana-pro-preview")
    panels = []
    panel_match = re.search(r'\[.*\]', panel_text, re.DOTALL)
    if panel_match:
        try:
            panels = json.loads(panel_match.group())
        except:
            panels = []
    if not panels or len(panels) != panels_count:
        panels = []
        for i in range(panels_count):
            panels.append({
                "panel_number": i+1,
                "description": story.get("plot", [f"Panel {i+1} description"])[i] if i < len(story.get("plot", [])) else f"Panel {i+1}",
                "characters_present": [c.split("-")[0].strip() for c in story.get("characters", [])],
                "suggested_art_style": user_style.get("overall_style", "cartoon")
            })

    dialogue_prompt = f"""
    You are a dialogue expert. For each panel description, add dialogue.
    Story: {json.dumps(story)}
    Panels: {json.dumps(panels)}
    {style_instruction}
    All dialogue MUST be in {language}.
    Return a JSON array of {panels_count} objects with fields: panel_number (int), dialogues (list of objects with character, text, bubble_type).
    """
    dialogue_text = call_gemini(dialogue_prompt, model="nano-banana-pro-preview")
    dialogues = []
    dialogue_match = re.search(r'\[.*\]', dialogue_text, re.DOTALL)
    if dialogue_match:
        try:
            dialogues = json.loads(dialogue_match.group())
        except:
            dialogues = []
    if not dialogues or len(dialogues) != panels_count:
        dialogues = []
        for i in range(panels_count):
            panel_dialogues = []
            for char in panels[i].get("characters_present", []):
                panel_dialogues.append({
                    "character": char,
                    "text": f"Dialogue for {char} in panel {i+1}",
                    "bubble_type": "speech"
                })
            dialogues.append({
                "panel_number": i+1,
                "dialogues": panel_dialogues
            })

    style_prompt = f"""
    You are a comic style advisor. Suggest an art style and language tone.
    Story: {json.dumps(story)}
    Panels: {json.dumps(panels)}
    User preferences: {json.dumps(user_style)}
    Respond in {language}.
    Return a JSON object with fields: overall_style (string), language_tone (string), color_palette (string).
    """
    style_text = call_gemini(style_prompt)
    style_advice = {}
    style_match = re.search(r'\{.*\}', style_text, re.DOTALL)
    if style_match:
        try:
            style_advice = json.loads(style_match.group())
        except:
            style_advice = {}
    if not style_advice:
        style_advice = {
            "overall_style": user_style.get("overall_style", "cartoon"),
            "language_tone": user_style.get("language_tone", "heartwarming"),
            "color_palette": user_style.get("color_palette", "warm")
        }

    return JSONResponse(content={"panels": panels, "dialogues": dialogues, "style_advice": style_advice})

@app.post("/generate-images")
async def generate_images(request: dict):
    panels = request.get("panels")
    style = request.get("style", {})
    dialogues = request.get("dialogues", [])
    language = request.get("language", "English")
    images = []

    for panel in panels:
        panel_dialogue = next((d for d in dialogues if d["panel_number"] == panel["panel_number"]), None)
        dialogue_lines = []
        if panel_dialogue:
            for d in panel_dialogue["dialogues"]:
                dialogue_lines.append(f"{d['character']}: \"{d['text']}\" ({d['bubble_type']} bubble)")

        prompt = f"""
Create a single comic panel illustration with the following details. The image MUST look like a panel from a comic book, with clear lines, vibrant colors, and speech bubbles integrated into the image.
- Scene description: {panel['description']}
- Characters present: {', '.join(panel['characters_present'])}
- Art style: {style.get('overall_style', 'whimsical watercolor')}
- Color palette: {style.get('color_palette', 'soft pastel')}
- Mood: {style.get('language_tone', 'heartwarming')}
- Dialogue to include as speech bubbles: {', '.join(dialogue_lines) if dialogue_lines else 'No dialogue'}
- The text in the speech bubbles MUST be in {language}.

The speech bubbles should be drawn in the appropriate style (round for speech, cloud for thought, jagged for shout, etc.) and placed near the speaking characters. The characters' expressions and poses should match the described action. The background should reflect the scene. Make it look like a professional comic page.
"""
        img_data = generate_image(prompt)
        images.append({
            "panel_number": panel['panel_number'],
            "image": img_data,
            "description": panel['description'][:100] + "..."
        })

    return JSONResponse(content={"images": images})

@app.post("/download-pdf")
async def download_pdf(request: dict):
    images = request.get("images", [])
    style_advice = request.get("style_advice", {})
    story_title = request.get("story_title", "Comic")
    timestamp = int(time.time())
    
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 100, story_title)
    c.setFont("Helvetica", 14)
    y = height - 150
    c.drawString(50, y, f"Style: {style_advice.get('overall_style', 'N/A')}")
    y -= 20
    c.drawString(50, y, f"Tone: {style_advice.get('language_tone', 'N/A')}")
    y -= 20
    c.drawString(50, y, f"Palette: {style_advice.get('color_palette', 'N/A')}")
    c.showPage()
    
    images.sort(key=lambda x: x["panel_number"])
    
    for img in images:
        if img.get("image"):
            img_data = base64.b64decode(img["image"])
            img_pil = PILImage.open(BytesIO(img_data))
            img_width, img_height = img_pil.size
            max_width = width - 100
            max_height = height - 200
            scale = min(max_width / img_width, max_height / img_height)
            draw_width = img_width * scale
            draw_height = img_height * scale
            x = (width - draw_width) / 2
            y = (height - draw_height - 50) / 2 + 50
            
            img_reader = ImageReader(img_pil)
            c.drawImage(img_reader, x, y, width=draw_width, height=draw_height)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, f"Panel {img['panel_number']}")
            c.showPage()
    
    c.save()
    buffer.seek(0)
    return Response(content=buffer.read(), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={story_title.replace(' ', '_')}_{timestamp}.pdf"})

@app.post("/download-booklet")
async def download_booklet(request: dict):
    images = request.get("images", [])
    style_advice = request.get("style_advice", {})
    story_title = request.get("story_title", "Comic")
    timestamp = int(time.time())
    
    buffer = BytesIO()
    booklet_page = landscape(A4)
    c = canvas.Canvas(buffer, pagesize=booklet_page)
    width, height = booklet_page
    
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 100, story_title)
    c.setFont("Helvetica", 14)
    y = height - 150
    c.drawString(50, y, f"Style: {style_advice.get('overall_style', 'N/A')}")
    y -= 20
    c.drawString(50, y, f"Tone: {style_advice.get('language_tone', 'N/A')}")
    y -= 20
    c.drawString(50, y, f"Palette: {style_advice.get('color_palette', 'N/A')}")
    c.showPage()
    
    images.sort(key=lambda x: x["panel_number"])
    
    for i in range(0, len(images), 2):
        # Left panel
        img_left = images[i]
        if img_left.get("image"):
            img_data = base64.b64decode(img_left["image"])
            img_pil = PILImage.open(BytesIO(img_data))
            img_width, img_height = img_pil.size
            max_width = (width / 2) - 40
            max_height = height - 150
            scale = min(max_width / img_width, max_height / img_height)
            draw_width = img_width * scale
            draw_height = img_height * scale
            x_left = 20
            y_center = (height - draw_height) / 2
            img_reader = ImageReader(img_pil)
            c.drawImage(img_reader, x_left, y_center, width=draw_width, height=draw_height)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(x_left, y_center - 20, f"Panel {img_left['panel_number']}")
        
        if i+1 < len(images):
            img_right = images[i+1]
            if img_right.get("image"):
                img_data = base64.b64decode(img_right["image"])
                img_pil = PILImage.open(BytesIO(img_data))
                img_width, img_height = img_pil.size
                max_width = (width / 2) - 40
                max_height = height - 150
                scale = min(max_width / img_width, max_height / img_height)
                draw_width = img_width * scale
                draw_height = img_height * scale
                x_right = width / 2 + 20
                y_center = (height - draw_height) / 2
                img_reader = ImageReader(img_pil)
                c.drawImage(img_reader, x_right, y_center, width=draw_width, height=draw_height)
                c.setFont("Helvetica-Bold", 12)
                c.drawString(x_right, y_center - 20, f"Panel {img_right['panel_number']}")
        c.showPage()
    
    c.save()
    buffer.seek(0)
    return Response(content=buffer.read(), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={story_title.replace(' ', '_')}_{timestamp}_booklet.pdf"})

if __name__ == "__main__":
    print("🚀 Multi-Agent Comic Studio with image upload running on http://localhost:8080")
    print("⚠️ Make sure GEMINI_API_KEY is set in environment")
    uvicorn.run(app, host="0.0.0.0", port=8080)
