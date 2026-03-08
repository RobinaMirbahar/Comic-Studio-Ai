from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import time
import uuid
import zipfile
import hashlib
from io import BytesIO
from datetime import datetime
from dotenv import load_dotenv
from agents.story_generator import StoryGeneratorAgent
from agents.panel_generator import PanelGeneratorAgent
from agents.download_handler import DownloadHandler
from agents.character_processor import CharacterProcessor
import socketio

# Load environment variables
load_dotenv()

# Check if API key is loaded
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ WARNING: GEMINI_API_KEY not found in environment variables")
else:
    print(f"✅ API key loaded")

# Create Socket.IO server
sio = socketio.AsyncServer(
    cors_allowed_origins='*',
    async_mode='asgi',
    ping_timeout=60,
    ping_interval=25
)

# Create FastAPI app
app = FastAPI(title="Comic Generator", version="2.0.0")

# Set up templates
templates = Jinja2Templates(directory="templates")

# Initialize agents
story_gen = StoryGeneratorAgent()
panel_gen = PanelGeneratorAgent()
download_handler = DownloadHandler()
char_processor = CharacterProcessor()

# Connect panel generator to character processor
panel_gen.set_character_processor(char_processor)

# Mount static files
os.makedirs("static/comics", exist_ok=True)
os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Languages
LANGUAGES = {
    "en": {"name": "English", "flag": "🇺🇸", "dir": "ltr"},
    "es": {"name": "Español", "flag": "🇪🇸", "dir": "ltr"},
    "fr": {"name": "Français", "flag": "🇫🇷", "dir": "ltr"},
    "de": {"name": "Deutsch", "flag": "🇩🇪", "dir": "ltr"},
    "it": {"name": "Italiano", "flag": "🇮🇹", "dir": "ltr"},
    "pt": {"name": "Português", "flag": "🇵🇹", "dir": "ltr"},
    "ja": {"name": "日本語", "flag": "🇯🇵", "dir": "ltr"},
    "zh": {"name": "中文", "flag": "🇨🇳", "dir": "ltr"},
    "ar": {"name": "العربية", "flag": "🇸🇦", "dir": "rtl"}
}

# Styles
STYLES = {
    "manga": {"name": "Japanese Manga", "icon": "🇯🇵"},
    "western": {"name": "Western Comic", "icon": "🇺🇸"},
    "watercolor": {"name": "Watercolor", "icon": "🎨"},
    "sketch": {"name": "Pencil Sketch", "icon": "✏️"},
    "anime": {"name": "Anime", "icon": "✨"},
    "vintage": {"name": "Vintage", "icon": "📰"}
}

# Panel options
PANEL_OPTIONS = [1, 2, 3, 4, 6, 9]

# Generate language options HTML
language_options = ""
for code, lang in LANGUAGES.items():
    language_options += f'<option value="{code}" data-dir="{lang["dir"]}">{lang["flag"]} {lang["name"]}</option>\n'

# Generate style options HTML
style_options = ""
for code, style in STYLES.items():
    style_options += f'<option value="{code}">{style["icon"]} {style["name"]}</option>\n'

# Generate panel options HTML
panel_options_html = ""
for num in PANEL_OPTIONS:
    panel_options_html += f'<option value="{num}">{num} Panels</option>\n'

# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    print(f'🔌 Client connected: {sid}')

@sio.event
async def disconnect(sid):
    print(f'🔌 Client disconnected: {sid}')

@sio.event
async def voice_command(sid, data):
    """Handle voice commands in real-time"""
    command = data.get('command', '').lower()
    print(f'🎤 Voice command from {sid}: "{command}"')
    
    # Process command
    if 'stop' in command or 'cancel' in command:
        await sio.emit('command_response', {
            'action': 'stop',
            'message': 'Stopping generation...'
        }, room=sid)
    elif 'new story' in command or 'start over' in command:
        await sio.emit('command_response', {
            'action': 'new_story',
            'message': 'Creating new story...'
        }, room=sid)
    elif 'generate' in command or 'make comic' in command:
        await sio.emit('command_response', {
            'action': 'generate',
            'message': 'Generating comic...'
        }, room=sid)
    elif 'read' in command or 'narrate' in command or 'speak' in command:
        await sio.emit('command_response', {
            'action': 'narrate',
            'message': 'Starting narration...'
        }, room=sid)

# Wrap FastAPI app with Socket.IO
socket_app = socketio.ASGIApp(sio, app)

# Character upload endpoint
@app.post("/api/upload-character")
async def upload_character(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        result = char_processor.save_character(contents, file.filename)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/characters")
async def get_characters():
    return JSONResponse(content={"characters": char_processor.get_all_characters()})

@app.delete("/api/characters/{char_id}")
async def delete_character(char_id: str):
    success = char_processor.delete_character(char_id)
    return JSONResponse(content={"success": success})

# Comic generation endpoint
@app.post("/generate")
async def generate_comic(request: dict):
    topic = request.get("topic", "")
    language = request.get("language", "en")
    
    if not topic:
        return JSONResponse(status_code=400, content={"error": "Topic required"})
    
    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = JobStatus(job_id)
    
    # Start background task
    import asyncio
    asyncio.create_task(process_comic_job(job_id, topic, language))
    
    return {"job_id": job_id, "status": "pending"}

# Store jobs in memory
jobs = {}

class JobStatus:
    def __init__(self, job_id):
        self.job_id = job_id
        self.status = "pending"
        self.progress = 0
        self.result = None
        self.error = None

async def process_comic_job(job_id, topic, language):
    try:
        jobs[job_id].status = "processing"
        jobs[job_id].progress = 30
        
        result = story_gen.create_comic(topic, language)
        
        jobs[job_id].progress = 80
        jobs[job_id].result = {
            "job_id": job_id,
            "title": result["title"],
            "pages": len(result["pages"]),
            "page_urls": result["pages"],
            "characters": result["characters"],
            "plot": result.get("plot", [])
        }
        jobs[job_id].status = "completed"
        jobs[job_id].progress = 100
        
    except Exception as e:
        jobs[job_id].status = "failed"
        jobs[job_id].error = str(e)

@app.get("/job/{job_id}")
async def get_job_status(job_id: str):
    if job_id not in jobs:
        return JSONResponse(status_code=404, content={"error": "Job not found"})
    
    job = jobs[job_id]
    return {
        "job_id": job.job_id,
        "status": job.status,
        "progress": job.progress,
        "result": job.result,
        "error": job.error
    }

# Download endpoints
@app.post("/download-zip")
async def download_zip(request: dict):
    try:
        pages = request.get("pages", [])
        title = request.get("title", "comic").replace(" ", "_")
        zip_buffer = download_handler.create_zip(pages, title)
        return Response(
            content=zip_buffer.getvalue(), 
            media_type="application/zip",
            headers={"Content-Disposition": f'attachment; filename="{title}.zip"'}
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/download-pdf")
async def download_pdf(request: dict):
    try:
        pages = request.get("pages", [])
        title = request.get("title", "comic").replace(" ", "_")
        language = request.get("language", "en")
        pdf_buffer = download_handler.create_pdf(pages, title, language)
        return Response(
            content=pdf_buffer.getvalue(), 
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{title}.pdf"'}
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/download-booklet")
async def download_booklet(request: dict):
    try:
        pages = request.get("pages", [])
        title = request.get("title", "comic").replace(" ", "_")
        pdf_buffer = download_handler.create_booklet(pages, title)
        return Response(
            content=pdf_buffer.getvalue(), 
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{title}_booklet.pdf"'}
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy"}

# Root endpoint with template
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "LANGUAGE_OPTIONS": language_options,
            "STYLE_OPTIONS": style_options,
            "PANEL_OPTIONS": panel_options_html
        }
    )

# Story generation endpoint
@app.post("/generate-story")
async def generate_story(request: dict):
    topic = request.get("topic", "")
    language = request.get("language", "en")
    story = story_gen.generate(topic)
    return JSONResponse(content=story)

# IMPORTANT: This is the ONLY generate-pages endpoint
@app.post("/generate-pages-with-characters")
async def generate_pages_with_characters(request: dict):
    story = request.get("story", {})
    language = request.get("language", "en")
    style = request.get("style", "manga")
    panels = request.get("panels", 4)
    character_ids = request.get("character_ids", [])
    prompt = request.get("prompt", "")
    
    print("\n" + "="*60)
    print(f"🎨 BACKEND RECEIVED PROMPT: '{prompt}'")
    print("="*60 + "\n")
    
    pages = panel_gen.generate_pages(
        story, 
        language=language, 
        style=style,
        prompt=prompt,
        character_ids=character_ids
    )
    return JSONResponse(content=pages)

# Bubble endpoint
@app.post("/add-bubble")
async def add_bubble(request: dict):
    try:
        from agents.bubble_drawer import BubbleDrawer
        
        image_url = request.get("image_url")
        text = request.get("text", "")
        bubble_type = request.get("bubble_type", "speech")
        emotion = request.get("emotion", "neutral")
        position = request.get("position", "bottom")
        panel_index = request.get("panel_index", 0)
        
        print(f"\n💬 Adding bubble to panel {panel_index+1}: {text}")
        
        bubble_drawer = BubbleDrawer()
        new_image_url = bubble_drawer.add_bubble(
            image_url, text, bubble_type, emotion, position
        )
        
        if new_image_url:
            return JSONResponse(content={"success": True, "new_image_url": new_image_url})
        else:
            return JSONResponse(content={"success": False, "error": "Failed to add bubble"})
            
    except Exception as e:
        print(f"❌ Error adding bubble: {e}")
        return JSONResponse(content={"success": False, "error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print("="*60)
    print("🎨 Multi-Agent Comic Generator with Live Voice")
    print("="*60)
    print(f"✅ Story Generator: Ready")
    print(f"✅ Panel Generator: Ready")
    print(f"✅ Download Handler: Ready")
    print(f"✅ Character Processor: Ready")
    print(f"✅ Socket.IO: Ready for live voice")
    print(f"🌐 Languages: {len(LANGUAGES)} supported")
    print(f"🎨 Styles: {len(STYLES)} supported")
    print(f"📐 Panel Options: {len(PANEL_OPTIONS)} supported")
    print(f"📱 URL: http://localhost:{port}")
    print("="*60)
    uvicorn.run(socket_app, host="0.0.0.0", port=port)
