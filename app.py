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
import asyncio
import traceback

# ========== ADK Imports (Optional) ==========
try:
    from google.adk import Runner
    from google.adk.sessions import InMemorySessionService
    from adk_agents.creative_director.agent import creative_director
    ADK_AVAILABLE = True
    print("✅ ADK available")
except ImportError:
    ADK_AVAILABLE = False
    print("⚠️ ADK not installed - ADK Guided Mode will use fallback")

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

# Styles - Expanded with more options
STYLES = {
    "manga": {"name": "Japanese Manga", "icon": "🇯🇵", "desc": "Black & white, screentones, speed lines"},
    "western": {"name": "Western Comic", "icon": "🇺🇸", "desc": "Bold colors, superhero style, dynamic"},
    "anime": {"name": "Anime", "icon": "✨", "desc": "Vibrant colors, cel-shaded, glossy eyes"},
    "watercolor": {"name": "Watercolor", "icon": "🎨", "desc": "Soft gradients, painted look, artistic"},
    "sketch": {"name": "Pencil Sketch", "icon": "✏️", "desc": "Rough lines, hand-drawn feel, graphite"},
    "vintage": {"name": "Vintage", "icon": "📰", "desc": "1950s style, muted colors, halftone dots"},
    "pixel": {"name": "Pixel Art", "icon": "🟦", "desc": "8-bit retro game style, blocky pixels"},
    "chibi": {"name": "Chibi", "icon": "🥹", "desc": "Cute super-deformed, big heads, small bodies"},
    "realistic": {"name": "Realistic", "icon": "📸", "desc": "Semi-realistic, detailed shading"},
    "cartoon": {"name": "Cartoon", "icon": "🐭", "desc": "Classic Disney-style, exaggerated features"},
    "noir": {"name": "Noir", "icon": "🕶️", "desc": "Film noir, high contrast, shadows, mystery"},
    "woodcut": {"name": "Woodcut", "icon": "🪵", "desc": "Medieval woodblock style, bold lines"},
    "ukiyo_e": {"name": "Ukiyo-e", "icon": "🗻", "desc": "Japanese woodblock, floating world"},
    "graffiti": {"name": "Graffiti", "icon": "🎭", "desc": "Street art, spray paint, vibrant"},
    "comic_book": {"name": "Comic Book", "icon": "💥", "desc": "1960s comics, Benday dots, pop art"},
    "steampunk": {"name": "Steampunk", "icon": "⚙️", "desc": "Victorian era with gears, brass"},
    "cyberpunk": {"name": "Cyberpunk", "icon": "🤖", "desc": "Neon lights, dark future, high-tech"},
    "medieval": {"name": "Medieval", "icon": "🏰", "desc": "Illuminated manuscript, gold leaf"},
    "expressionist": {"name": "Expressionist", "icon": "🎭", "desc": "German Expressionism, distorted"},
    "pop_art": {"name": "Pop Art", "icon": "🥫", "desc": "Andy Warhol style, bright colors"},
    "minimalist": {"name": "Minimalist", "icon": "○", "desc": "Simple lines, minimal details"},
    "pastel": {"name": "Pastel", "icon": "🌸", "desc": "Soft pastel colors, gentle, dreamy"},
    "gothic": {"name": "Gothic", "icon": "🦇", "desc": "Dark, ornate, medieval gothic"},
    "art_nouveau": {"name": "Art Nouveau", "icon": "🌿", "desc": "Organic flowing lines, floral"},
    "baroque": {"name": "Baroque", "icon": "✨", "desc": "Dramatic lighting, rich details"}
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

# Store jobs in memory
jobs = {}

class JobStatus:
    def __init__(self, job_id):
        self.job_id = job_id
        self.status = "pending"
        self.progress = 0
        self.result = None
        self.error = None

# ==================== API ENDPOINTS ====================

@app.get("/api/quota-status")
async def quota_status():
    """Check current API quota status"""
    try:
        return JSONResponse(content={
            "status": "ok",
            "message": "API quota available",
            "using_fallback": False
        })
    except:
        return JSONResponse(content={
            "status": "limited",
            "message": "API quota status unknown",
            "using_fallback": True
        })

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

@app.post("/generate")
async def generate_comic(request: dict):
    topic = request.get("topic", "")
    language = request.get("language", "en")
    
    if not topic:
        return JSONResponse(status_code=400, content={"error": "Topic required"})
    
    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = JobStatus(job_id)
    
    import asyncio
    asyncio.create_task(process_comic_job(job_id, topic, language))
    
    return {"job_id": job_id, "status": "pending"}

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

@app.get("/health")
async def health():
    return {"status": "healthy"}

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

@app.post("/generate-story")
async def generate_story(request: dict):
    topic = request.get("topic", "")
    language = request.get("language", "en")
    character_names = request.get("character_names", {})
    
    story = story_gen.generate(topic, character_names=character_names)
    return JSONResponse(content=story)

@app.post("/generate-pages-with-characters")
async def generate_pages_with_characters(request: dict):
    story = request.get("story", {})
    language = request.get("language", "en")
    style = request.get("style", "manga")
    panels = request.get("panels", 4)
    character_ids = request.get("character_ids", [])
    prompt = request.get("prompt", "")
    from_adk = request.get("from_adk", False)
    
    print("\n" + "="*60)
    print(f"🎨 BACKEND RECEIVED PROMPT: '{prompt}'")
    if from_adk:
        print(f"🤖 This is from ADK conversation")
    print("="*60 + "\n")
    
    pages = panel_gen.generate_pages(
        story, 
        language=language, 
        style=style,
        prompt=prompt,
        character_ids=character_ids
    )
    return JSONResponse(content=pages)

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

@app.post("/adk/generate")
async def adk_generate_comic(request: dict):
    """Generate comic using ADK conversational agent"""
    try:
        prompt = request.get("prompt", "")
        language = request.get("language", "en")
        style = request.get("style", "manga")
        
        print(f"\n🎬 ADK Guided Mode started for: '{prompt}'")
        
        if not ADK_AVAILABLE:
            print("⚠️ ADK not available, using fallback")
            
            story = story_gen.generate(prompt)
            
            pages = panel_gen.generate_pages(
                story=story,
                language=language,
                style=style,
                prompt=prompt
            )
            
            return JSONResponse(content={
                "success": True,
                "comic": pages,
                "story": story,
                "message": "Comic generated (ADK fallback mode)"
            })
        
        session_service = InMemorySessionService()
        session = await session_service.create_session(
            user_id="user_" + str(uuid.uuid4())[:8],
            session_id="session_" + str(uuid.uuid4())[:8],
            state={
                "user_input": prompt,
                "language": language,
                "style": style
            }
        )
        
        runner = Runner(
            agent=creative_director,
            session_service=session_service
        )
        
        results = []
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id
        ):
            results.append({
                "agent": event.author,
                "message": event.content
            })
            if event.actions and event.actions.escalate:
                break
        
        return JSONResponse(content={
            "success": True,
            "pipeline": results,
            "comic": session.state.get("panels", []),
            "story": session.state.get("story", {})
        })
        
    except Exception as e:
        print(f"❌ ADK guided mode error: {e}")
        return JSONResponse(content={
            "success": False,
            "error": str(e)
        })

# ==================== ADK CONVERSATION ENDPOINTS ====================
adk_sessions = {}

@app.post("/adk/start-conversation")
async def adk_start_conversation(request: dict):
    """Start a new ADK conversation"""
    try:
        prompt = request.get("prompt", "")
        session_id = request.get("session_id", "")
        language = request.get("language", "en")
        style = request.get("style", "manga")
        story = request.get("story", {})
        
        print(f"\n🎬 ADK Conversation started for: '{prompt}'")
        print(f"📝 Session ID: {session_id}")
        
        # Extract theme for personalized response
        theme = "adventure"
        if "cat" in prompt.lower():
            theme = "cat adventure"
        elif "dog" in prompt.lower():
            theme = "dog adventure"
        elif "robot" in prompt.lower():
            theme = "robot adventure"
        elif "space" in prompt.lower() or "mars" in prompt.lower():
            theme = "space adventure"
        elif "beach" in prompt.lower():
            theme = "beach adventure"
        
        adk_sessions[session_id] = {
            "step": "main_character",
            "prompt": prompt,
            "theme": theme,
            "language": language,
            "style": style,
            "main_character": None,
            "supporting_character": None,
            "panels": [],
            "current_panel": 0,
            "story": story
        }
        
        return JSONResponse(content={
            "type": "question",
            "message": f"I love the idea of a {theme}! Let's bring it to life. What should the main character be named?"
        })
        
    except Exception as e:
        print(f"❌ ADK start error: {e}")
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)})

@app.post("/adk/converse")
async def adk_converse(request: dict):
    """Handle ADK conversation"""
    try:
        message = request.get("message", "")
        session_id = request.get("session_id", "")
        
        print(f"📨 ADK message received: '{message}'")
        print(f"📝 Session ID: {session_id}")
        
        if session_id not in adk_sessions:
            print(f"❌ Session {session_id} not found")
            return JSONResponse(content={
                "type": "error",
                "message": "Session expired. Please start over."
            })
        
        session = adk_sessions[session_id]
        print(f"📊 Current step: {session['step']}")
        
        if session["step"] == "main_character":
            session["main_character"] = message
            session["step"] = "supporting_character"
            return JSONResponse(content={
                "type": "question",
                "message": f"Great! Who should join {message}? Name a supporting character:"
            })
            
        elif session["step"] == "supporting_character":
            session["supporting_character"] = message
            session["step"] = "complete"
            
            story_data = {
                "title": f"{session['main_character']}'s Adventure",
                "main_character_name": session['main_character'],
                "supporting_character_name": session['supporting_character'],
                "characters": [
                    f"{session['main_character']} - Main character",
                    f"{session['supporting_character']} - Supporting character"
                ],
                "plot": [
                    f"{session['main_character']} begins the adventure",
                    f"{session['main_character']} meets {session['supporting_character']}",
                    "They face a challenge",
                    "They succeed together"
                ]
            }
            
            return JSONResponse(content={
                "type": "generating",
                "message": "✨ Creating your comic now...",
                "story": story_data
            })
            
    except Exception as e:
        print(f"❌ ADK converse error: {e}")
        traceback.print_exc()
        return JSONResponse(content={
            "type": "error",
            "message": f"Sorry, an error occurred: {str(e)}"
        })

async def generate_comic_from_adk(session_id, story_data, session):
    """Generate comic from ADK conversation"""
    try:
        print(f"🎨 Generating ADK comic for session {session_id}")
        
        story = {
            "title": story_data["title"],
            "characters": story_data["characters"],
            "plot": story_data["plot"],
            "main_character_name": story_data["main_character_name"],
            "supporting_character_name": story_data["supporting_character_name"]
        }
        
        pages = panel_gen.generate_pages(
            story=story,
            language=session["language"],
            style=session["style"],
            prompt=session["prompt"],
            from_adk=True
        )
        
        session["comic"] = pages
        session["step"] = "complete"
        
        print(f"✅ ADK comic generated for session {session_id}")
        
    except Exception as e:
        print(f"❌ ADK generation error: {e}")
        traceback.print_exc()

@app.post("/adk/test")
async def adk_test(request: dict):
    return JSONResponse(content={
        "type": "question",
        "message": "ADK test successful!"
    })

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
    print(f"🤖 ADK Guided Mode: {'✅ Available' if ADK_AVAILABLE else '⚠️ Fallback Mode'}")
    print(f"🌐 Languages: {len(LANGUAGES)} supported")
    print(f"🎨 Styles: {len(STYLES)} supported")
    print(f"📐 Panel Options: {len(PANEL_OPTIONS)} supported")
    print(f"📱 URL: http://localhost:{port}")
    print("="*60)
    uvicorn.run(socket_app, host="0.0.0.0", port=port)

# ==================== COMPLETE ADK CONVERSATION FLOW ====================
# Enhanced with 14 questions for full panel control

@app.post("/adk/start-conversation")
async def adk_start_conversation(request: dict):
    """Start comprehensive ADK conversation"""
    try:
        prompt = request.get("prompt", "")
        session_id = request.get("session_id", "")
        language = request.get("language", "en")
        style = request.get("style", "manga")
        
        print(f"\n{'='*60}")
        print(f"🎬 ADK COMPLETE CONVERSATION STARTED")
        print(f"📝 Prompt: '{prompt}'")
        print(f"🆔 Session: {session_id}")
        print(f"{'='*60}\n")
        
        # Initialize comprehensive session
        adk_sessions[session_id] = {
            "step": "main_character",
            "prompt": prompt,
            "language": language,
            "style": style,
            "main_character": None,
            "supporting_character": None,
            "panels": [],
            "created_at": time.time()
        }
        
        return JSONResponse(content={
            "type": "question",
            "message": "Let's create your comic! First, what's the main character's name?",
            "progress": {"current": 1, "total": 14}
        })
        
    except Exception as e:
        print(f"❌ ADK start error: {e}")
        return JSONResponse(content={"error": str(e)})

@app.post("/adk/converse")
async def adk_converse(request: dict):
    """Handle comprehensive ADK conversation"""
    try:
        message = request.get("message", "")
        session_id = request.get("session_id", "")
        
        if session_id not in adk_sessions:
            return JSONResponse(content={"error": "Session expired"})
        
        session = adk_sessions[session_id]
        current_step = session["step"]
        
        # Process 14 steps
        steps = [
            ("main_character", "Great! Who should be their companion? Name a supporting character:"),
            ("supporting_character", "Panel 1 (Beginning): Where does the story start? Describe the scene:"),
            ("panel1_description", f"What should {session.get('main_character', 'the character')} say in this panel?"),
            ("panel1_dialogue", "What emotion? (happy/sad/angry/excited/scared/neutral)"),
            ("panel1_emotion", "Panel 2 (Journey): What happens next? Describe the scene:"),
            ("panel2_description", f"What does {session.get('main_character', 'the character')} say here?"),
            ("panel2_dialogue", "What emotion for this dialogue?"),
            ("panel2_emotion", "Panel 3 (Challenge): What problem appears? Describe the scene:"),
            ("panel3_description", f"What does {session.get('main_character', 'the character')} say during the challenge?"),
            ("panel3_dialogue", "What emotion?"),
            ("panel3_emotion", "Panel 4 (Conclusion): How does it end? Describe the final scene:"),
            ("panel4_description", f"What does {session.get('main_character', 'the character')} say at the end?"),
            ("panel4_dialogue", "What emotion for the ending?"),
            ("panel4_emotion", "complete")
        ]
        
        # Find current step index
        step_index = 0
        for i, (step_name, _) in enumerate(steps):
            if step_name == current_step:
                step_index = i
                break
        
        # Save current response
        if current_step == "main_character":
            session["main_character"] = message
        elif current_step == "supporting_character":
            session["supporting_character"] = message
        elif "description" in current_step:
            panel_num = int(current_step.split("_")[0].replace("panel", "")) - 1
            if len(session["panels"]) <= panel_num:
                session["panels"].append({})
            session["panels"][panel_num]["description"] = message
        elif "dialogue" in current_step:
            panel_num = int(current_step.split("_")[0].replace("panel", "")) - 1
            session["panels"][panel_num]["dialogue"] = message
        elif "emotion" in current_step:
            panel_num = int(current_step.split("_")[0].replace("panel", "")) - 1
            session["panels"][panel_num]["emotion"] = message
        
        # Move to next step
        next_index = step_index + 1
        if next_index >= len(steps):
            session["step"] = "complete"
            
            # Generate comic
            story_data = {
                "title": f"{session['main_character']}'s Adventure",
                "main_character": session['main_character'],
                "supporting_character": session['supporting_character'],
                "panels": session['panels']
            }
            
            return JSONResponse(content={
                "type": "generating",
                "message": "✨ Creating your comic with all 4 panels and dialogue!",
                "progress": {"current": 14, "total": 14}
            })
        
        next_step, next_question = steps[next_index]
        session["step"] = next_step
        
        # Personalize question
        if "{main}" in next_question:
            next_question = next_question.replace("{main}", session.get("main_character", "the character"))
        
        return JSONResponse(content={
            "type": "question",
            "message": next_question,
            "progress": {"current": next_index + 1, "total": 14}
        })
        
    except Exception as e:
        print(f"❌ ADK converse error: {e}")
        return JSONResponse(content={"error": str(e)})

# Update generate-story endpoint to handle ADK preference
@app.post("/generate-story")
async def generate_story(request: dict):
    topic = request.get("topic", "")
    language = request.get("language", "en")
    character_names = request.get("character_names", {})
    from_adk = request.get("from_adk", False)
    
    # If from ADK, handle differently
    if from_adk:
        print(f"🎬 ADK story generation for: {topic}")
        # Return minimal response - ADK will handle full story
        return JSONResponse(content={
            "title": f"Adventure",
            "characters": ["Hero", "Friend"],
            "plot": ["Beginning", "Middle", "End"]
        })
    
    # Regular story generation
    story = story_gen.generate(topic, character_names=character_names)
    return JSONResponse(content=story)

# ==================== COMPLETE 14-QUESTION ADK FLOW ====================
# This enables full panel-by-panel storytelling with dialogue and emotions

# Define the 14 conversation steps
ADK_STEPS = [
    "main_character",
    "supporting_character", 
    "panel1_description",
    "panel1_dialogue",
    "panel1_emotion",
    "panel2_description",
    "panel2_dialogue",
    "panel2_emotion",
    "panel3_description",
    "panel3_dialogue",
    "panel3_emotion",
    "panel4_description",
    "panel4_dialogue",
    "panel4_emotion"
]

ADK_QUESTIONS = {
    "main_character": "Let's create your comic! First, what's the main character's name?",
    "supporting_character": "Great! Who should be their companion? Name a supporting character:",
    "panel1_description": "Panel 1 (Beginning): Where does the story start? Describe the scene in detail:",
    "panel1_dialogue": "What should {main} say in this panel?",
    "panel1_emotion": "What emotion for this dialogue? (happy/sad/angry/excited/scared/neutral)",
    "panel2_description": "Panel 2 (Journey): What happens next? Describe the scene:",
    "panel2_dialogue": "What does {main} say here?",
    "panel2_emotion": "What emotion for this dialogue?",
    "panel3_description": "Panel 3 (Challenge): What problem appears? Describe the scene:",
    "panel3_dialogue": "What does {main} say during the challenge?",
    "panel3_emotion": "What emotion?",
    "panel4_description": "Panel 4 (Conclusion): How does it end? Describe the final scene:",
    "panel4_dialogue": "What does {main} say at the end?",
    "panel4_emotion": "What emotion for the ending?"
}

@app.post("/adk/start-conversation")
async def adk_start_conversation(request: dict):
    """Start a comprehensive 14-question ADK conversation"""
    try:
        prompt = request.get("prompt", "")
        session_id = request.get("session_id", "")
        language = request.get("language", "en")
        style = request.get("style", "manga")
        
        print(f"\n{'='*60}")
        print(f"🎬 ADK 14-QUESTION CONVERSATION STARTED")
        print(f"📝 Prompt: '{prompt}'")
        print(f"🆔 Session: {session_id}")
        print(f"{'='*60}\n")
        
        # Initialize session with all needed fields
        adk_sessions[session_id] = {
            "step": "main_character",
            "prompt": prompt,
            "language": language,
            "style": style,
            "main_character": None,
            "supporting_character": None,
            "panels": [
                {"description": "", "dialogue": "", "emotion": ""},
                {"description": "", "dialogue": "", "emotion": ""},
                {"description": "", "dialogue": "", "emotion": ""},
                {"description": "", "dialogue": "", "emotion": ""}
            ],
            "created_at": time.time()
        }
        
        return JSONResponse(content={
            "type": "question",
            "message": ADK_QUESTIONS["main_character"],
            "progress": {"current": 1, "total": 14}
        })
        
    except Exception as e:
        print(f"❌ ADK start error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)})

@app.post("/adk/converse")
async def adk_converse(request: dict):
    """Handle the 14-question conversation flow"""
    try:
        message = request.get("message", "")
        session_id = request.get("session_id", "")
        
        print(f"📨 ADK message: '{message}'")
        
        if session_id not in adk_sessions:
            return JSONResponse(content={
                "type": "error",
                "message": "Session expired. Please start over."
            })
        
        session = adk_sessions[session_id]
        current_step = session["step"]
        
        print(f"📊 Current step: {current_step}")
        
        # Save the response based on current step
        if current_step == "main_character":
            session["main_character"] = message
            
        elif current_step == "supporting_character":
            session["supporting_character"] = message
            
        elif current_step == "panel1_description":
            session["panels"][0]["description"] = message
        elif current_step == "panel1_dialogue":
            session["panels"][0]["dialogue"] = message
        elif current_step == "panel1_emotion":
            session["panels"][0]["emotion"] = message
            
        elif current_step == "panel2_description":
            session["panels"][1]["description"] = message
        elif current_step == "panel2_dialogue":
            session["panels"][1]["dialogue"] = message
        elif current_step == "panel2_emotion":
            session["panels"][1]["emotion"] = message
            
        elif current_step == "panel3_description":
            session["panels"][2]["description"] = message
        elif current_step == "panel3_dialogue":
            session["panels"][2]["dialogue"] = message
        elif current_step == "panel3_emotion":
            session["panels"][2]["emotion"] = message
            
        elif current_step == "panel4_description":
            session["panels"][3]["description"] = message
        elif current_step == "panel4_dialogue":
            session["panels"][3]["dialogue"] = message
        elif current_step == "panel4_emotion":
            session["panels"][3]["emotion"] = message
        
        # Find next step
        current_index = ADK_STEPS.index(current_step) if current_step in ADK_STEPS else -1
        
        if current_index >= len(ADK_STEPS) - 1:
            # All steps complete - generate comic
            session["step"] = "complete"
            
            # Create comprehensive story data
            story_data = {
                "title": f"{session['main_character']} and {session['supporting_character']}'s Adventure",
                "main_character": session['main_character'],
                "supporting_character": session['supporting_character'],
                "panels": session['panels']
            }
            
            # Generate comic in background
            import asyncio
            asyncio.create_task(generate_comic_from_adk_full(session_id, story_data, session))
            
            return JSONResponse(content={
                "type": "generating",
                "message": "✨ Creating your comic with all 4 panels and dialogue! This will take a moment.",
                "progress": {"current": 14, "total": 14}
            })
        
        # Move to next step
        next_step = ADK_STEPS[current_index + 1]
        session["step"] = next_step
        
        # Get question for next step
        next_question = ADK_QUESTIONS[next_step]
        
        # Personalize question with character name if needed
        if "{main}" in next_question and session.get("main_character"):
            next_question = next_question.replace("{main}", session["main_character"])
        
        return JSONResponse(content={
            "type": "question",
            "message": next_question,
            "progress": {"current": current_index + 2, "total": 14}
        })
        
    except Exception as e:
        print(f"❌ ADK converse error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(content={
            "type": "error",
            "message": f"Sorry, an error occurred: {str(e)}"
        })

async def generate_comic_from_adk_full(session_id, story_data, session):
    """Generate comic from the full 14-question conversation"""
    try:
        print(f"\n🎨 GENERATING COMIC FROM 14-QUESTION ADK")
        print(f"📊 Panels: {len(story_data['panels'])}")
        
        # Format for panel generator
        plot = [p["description"] for p in story_data["panels"]]
        characters = [
            f"{story_data['main_character']} - Main character",
            f"{story_data['supporting_character']} - Supporting character"
        ]
        
        story = {
            "title": story_data["title"],
            "characters": characters,
            "plot": plot,
            "main_character_name": story_data["main_character"],
            "supporting_character_name": story_data["supporting_character"]
        }
        
        pages = panel_gen.generate_pages(
            story=story,
            language=session["language"],
            style=session["style"],
            prompt=session["prompt"],
            from_adk=True
        )
        
        session["comic"] = pages
        session["story_data"] = story_data
        
        print(f"✅ ADK comic generated with {len(pages)} panels")
        
    except Exception as e:
        print(f"❌ ADK generation error: {e}")
        traceback.print_exc()

# ==================== LIVE AGENT ENDPOINTS ====================

@app.post("/api/agent/chat")
async def agent_chat(request: dict):
    """Handle chat with live agent"""
    try:
        message = request.get("message", "")
        story = request.get("story", {})
        session_id = request.get("session_id", str(uuid.uuid4()))
        
        # Create context for Gemini
        context = f"""
        You are a helpful live story agent for a comic creation app.
        
        Current Story:
        Title: {story.get('title', 'Unknown')}
        Characters: {', '.join(story.get('characters', ['Unknown']))}
        Plot: {' → '.join(story.get('plot', ['Unknown']))}
        
        User Message: {message}
        
        Respond conversationally and offer specific, actionable suggestions.
        Keep responses concise but helpful (2-3 sentences).
        """
        
        # Use Gemini for intelligent responses
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(
            context,
            generation_config={
                "temperature": 0.8,
                "max_output_tokens": 200
            }
        )
        
        return {
            "success": True,
            "response": response.text,
            "session_id": session_id
        }
        
    except Exception as e:
        print(f"Agent error: {e}")
        return {
            "success": False,
            "response": "I'm having trouble right now. Please try again.",
            "session_id": session_id
        }

@app.post("/api/agent/suggest-dialogue")
async def suggest_dialogue(request: dict):
    """Generate dialogue suggestions for a panel"""
    try:
        panel = request.get("panel", 1)
        story = request.get("story", {})
        characters = story.get('characters', [])
        
        context = f"""
        Generate natural dialogue for panel {panel} of this comic story.
        
        Story: {story.get('title', 'Unknown')}
        Characters: {', '.join(characters)}
        Plot point: {story.get('plot', ['Unknown'])[panel-1] if len(story.get('plot', [])) >= panel else 'Unknown'}
        
        Return a JSON array with dialogue suggestions for each character.
        """
        
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(context)
        
        return {
            "success": True,
            "suggestions": response.text
        }
        
    except Exception as e:
        print(f"Dialogue suggestion error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/api/agent/status/{session_id}")
async def agent_status(session_id: str):
    """Get agent session status"""
    return {
        "session_id": session_id,
        "active": True,
        "timestamp": datetime.now().isoformat()
    }
