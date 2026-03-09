# 📖 Comic Studio AI - Usage Guide

## 📋 Table of Contents
- [Quick Start](#quick-start)
- [🎨 Your First Comic - Visual Guide](#-your-first-comic---visual-guide)
- [Web Interface Guide](#web-interface-guide)
- [API Usage Guide](#api-usage-guide)
- [Voice Commands](#voice-commands)
- [Character Upload](#character-upload)
- [Bubble Editor](#bubble-editor)
- [Download Options](#download-options)
- [Art Styles](#art-styles)
- [Languages](#languages)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### 1. **Start the Server**
```bash
# Make sure you're in the project directory
cd Comic-Studio-Ai

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the app
python app.py
```

### 2. **Open in Browser**
```
http://localhost:8080
```

---

## 🎨 Your First Comic - Visual Guide

### Step 1: Enter a Prompt
Type your idea in the text area. For example: **"mouse on road"**

```
┌─────────────────────────────────────┐
│ [mouse on road]                     │
│ [Generate Story] [Generate Comic]   │
└─────────────────────────────────────┘
```
*Enter your creative idea in the prompt box*

### Step 2: Generate Story
Click **"Generate Story"** and wait 2-3 seconds

```
┌─────────────────────────────────────┐
│ 📖 Generated Story                   │
│                                      │
│ The Amazing Adventure                │
│ Hero • Wise Guide • Curious Friend  │
│                                      │
│ 1. Once upon a time...              │
│ 2. Our hero discovered...           │
│ 3. Together they embarked...        │
│ 4. In the end they found...         │
└─────────────────────────────────────┘
```
*AI generates a complete story with characters and plot*

### Step 3: Generate Comic
Click **"Generate Comic"** and watch the magic happen!

```
┌─────────────┐ ┌─────────────┐
│   Panel 1   │ │   Panel 2   │
│             │ │             │
│    🐭       │ │    🚗       │
│  "I need to │ │  "Watch     │
│   cross!"   │ │   out!"     │
└─────────────┘ └─────────────┘
┌─────────────┐ ┌─────────────┐
│   Panel 3   │ │   Panel 4   │
│             │ │             │
│    🧀       │ │    🏁       │
│  "Almost    │ │  "I made    │
│   there!"   │ │   it!"      │
└─────────────┘ └─────────────┘
```
*4 comic panels appear with auto-generated speech bubbles*

### Step 4: Your Complete Comic! 🎉

| Before | After |
|--------|-------|
| Just text: "mouse on road" | 🖼️ **4 Complete Comic Panels** |
| | • Consistent mouse character |
| | • 4-part story progression |
| | • Auto-generated speech bubbles |

---

### 📸 Example Gallery

#### Example 1: "mouse on road"
| Panel 1 | Panel 2 | Panel 3 | Panel 4 |
|---------|---------|---------|---------|
| Mouse spots cheese | Crosses road | Narrow escape | Enjoys cheese |
| "I need that!" | "Here I go!" | "That was close!" | "Totally worth it!" |

#### Example 2: "cat astronaut on moon"
| Panel 1 | Panel 2 | Panel 3 | Panel 4 |
|---------|---------|---------|---------|
| Cat in spaceship | Lands on moon | Plants flag | Waves at Earth |
| "3..2..1.." | "One small step" | "For cats everywhere!" | "Meow from space!" |

#### Example 3: "dragon eating pizza"
| Panel 1 | Panel 2 | Panel 3 | Panel 4 |
|---------|---------|---------|---------|
| Dragon sees pizza | Takes a bite | Loves it! | Orders more |
| "What's this?" | "MMM!" | "Best thing ever!" | "I'll take 10!" |

---

### 🎯 Visual Workflow

```mermaid
graph LR
    A[📝 "mouse on road"] --> B[📖 Generated Story]
    B --> C[🎨 4 Comic Panels]
    
    style A fill:#e1f5fe,stroke:#01579b
    style B fill:#fff3e0,stroke:#bf360c
    style C fill:#e8f5e8,stroke:#1b5e20
```

---

### 📱 What You'll See

**Before Generation:**
```
┌─────────────────────────────────────┐
│ Enter your comic idea...            │
│ [mouse on road]                      │
│                                      │
│ [Generate Story] [Generate Comic]    │
└─────────────────────────────────────┘
```

**During Generation:**
```
┌─────────────────────────────────────┐
│ ⏳ Generating...                     │
│    🤖 Story Agent working...         │
└─────────────────────────────────────┘
```

**After Generation:**
```
┌─────────────────────────────────────┐
│ 📖 Story Generated!                  │
│ 🎨 4 Comic Panels Ready!             │
│ 💬 Speech Bubbles Added!             │
└─────────────────────────────────────┘
```

---

## 🖥️ Web Interface Guide

### Main Interface Sections

```
┌─────────────────────────────────────────────┐
│  HEADER                                     │
│  Title, badges, creator info                │
├─────────────────────────────────────────────┤
│  OPTIONS BAR                                │
│  Language • Style • Panels                  │
├─────────────────────────────────────────────┤
│  CHARACTER UPLOAD                           │
│  Upload and select custom characters        │
├─────────────────────────────────────────────┤
│  PROMPT INPUT                               │
│  [ Enter your idea here ]                   │
│  [Generate Story] [Generate Comic]          │
├─────────────────────────────────────────────┤
│  EXTRA BUTTONS                              │
│  Voice • New Story • Read Aloud • Stop     │
│  Share • Storyboard • Download • Bubbles   │
├─────────────────────────────────────────────┤
│  AGENT PIPELINE                             │
│  [Story] [Director] [Panel] status         │
├─────────────────────────────────────────────┤
│  RESULTS                                    │
│  Generated Story & 4 Comic Panels          │
└─────────────────────────────────────────────┘
```

### Step-by-Step Walkthrough

#### **Step 1: Enter a Prompt**
Type your idea in the text area. Examples:
- `mouse on road`
- `dragon eating pizza`
- `cat astronaut on moon`
- `robot teaching math`

#### **Step 2: Generate Story**
Click **"Generate Story"** and wait 2-3 seconds. You'll see:
- Story title
- Character descriptions
- 4 plot points

#### **Step 3: Generate Comic**
Click **"Generate Comic"** and wait 3-4 seconds. You'll see:
- 4 comic panels with your characters
- Auto-generated speech bubbles
- Consistent character appearance

#### **Step 4: Edit Bubbles (Optional)**
1. Click **"Add Bubbles"**
2. Select a panel (1-4)
3. Choose bubble type and emotion
4. Enter text or click **"AI Suggest"**
5. Click **"Apply to Panel"**

#### **Step 5: Download Your Comic**
Choose your format:
- **📦 ZIP** - All images in one archive
- **📄 PDF** - Professional document
- **📚 Booklet** - Print-ready booklet

---

## 📡 API Usage Guide

### Base URL
```
http://localhost:8080
```

### 1. **Generate Story**
```bash
curl -X POST http://localhost:8080/generate-story \
  -H "Content-Type: application/json" \
  -d '{"topic": "mouse on road", "language": "en"}'
```

### 2. **Generate Comic**
```bash
curl -X POST http://localhost:8080/generate-pages-with-characters \
  -H "Content-Type: application/json" \
  -d '{
    "story": {
      "title": "Mouse Adventure",
      "characters": ["Montgomery"],
      "plot": ["Start", "Middle", "Climax", "End"]
    },
    "style": "manga",
    "prompt": "mouse on road"
  }'
```

### 3. **Add Bubble**
```bash
curl -X POST http://localhost:8080/add-bubble \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "/static/comics/page_1.png",
    "text": "I need to cross this road!",
    "bubble_type": "speech",
    "emotion": "excited"
  }'
```

### 4. **Download as PDF**
```bash
curl -X POST http://localhost:8080/download-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "pages": [
      "/static/comics/page_1.png",
      "/static/comics/page_2.png",
      "/static/comics/page_3.png",
      "/static/comics/page_4.png"
    ],
    "title": "My Comic"
  }' \
  --output comic.pdf
```

### 5. **Upload Character**
```bash
curl -X POST http://localhost:8080/api/upload-character \
  -F "file=@/path/to/character.jpg"
```

---

## 🎤 Voice Commands

### Using Voice Input

1. Click the **🎤 Voice Input** button
2. The button turns red and says "Listening..."
3. Speak your command clearly
4. Wait 2 seconds for processing

### Supported Commands

| Command | Action |
|---------|--------|
| `"stop"` or `"cancel"` | Stops current generation |
| `"new story"` | Resets everything |
| `"generate comic"` | Starts comic generation |
| `"read aloud"` or `"narrate"` | Reads the story |
| Any other phrase | Fills the prompt box |

### Voice Tips
- Speak clearly at normal volume
- Wait for the "Listening..." indicator
- Commands work mid-sentence
- Voice input times out after 10 seconds

---

## 🎭 Character Upload

### How to Upload

1. Click the **upload area** in the "Upload Your Characters" section
2. Select an image (PNG, JPG, GIF, max 5MB)
3. The character appears as a thumbnail
4. **Click the thumbnail** to select it for generation

### Using Uploaded Characters

1. Select character(s) by clicking their thumbnails
2. Generate a comic as usual
3. The AI will try to incorporate your characters
4. Characters appear in all 4 panels

### Character Tips
- Use clear, front-facing images
- Simple characters work best
- Cartoon style images work better than photos
- You can select multiple characters

---

## 💬 Bubble Editor

### Bubble Types

| Type | Best For |
|------|----------|
| **🗣️ Speech** | Normal dialogue |
| **💭 Thought** | Inner thoughts |
| **📢 Shout** | Exclamations |
| **🤫 Whisper** | Quiet speech |
| **📖 Narration** | Story narration |
| **💥 SFX** | Sound effects |

### Emotions

| Emotion | Effect |
|---------|--------|
| 😊 Happy | Adds smile emoji |
| 😢 Sad | Adds tear emoji |
| 😠 Angry | Adds angry emoji |
| 🤩 Excited | Adds star eyes |
| 😨 Scared | Adds fear emoji |
| 😐 Neutral | No emoji |

### Positions

| Position | Description |
|----------|-------------|
| **Top** | Top center of panel |
| **Bottom** | Bottom center (default) |
| **Left** | Left side, centered |
| **Right** | Right side, centered |
| **Auto** | AI chooses best spot |

### Editing Steps

1. Click **"Add Bubbles"**
2. Select panel number (1-4)
3. Choose bubble type
4. Select emotion
5. Choose position
6. Enter text or click **"AI Suggest"**
7. Click **"Apply to Panel"**

---

## 📥 Download Options

### ZIP Download
- All 4 panels as individual PNG files
- Preserves original quality
- Good for editing

### PDF Download
- All panels in one document
- Professional layout
- Good for sharing

### Booklet Download
- 2 panels per page (front/back)
- Ready for printing
- Booklet format

---

## 🎨 Art Styles

| Style | Description | Best For |
|-------|-------------|----------|
| 🇯🇵 **Manga** | Black & white, screentones | Japanese comics |
| 🇺🇸 **Western** | Bold colors, superhero | American comics |
| ✨ **Anime** | Vibrant, cel-shaded | Japanese animation |
| ✏️ **Sketch** | Pencil, rough lines | Concept art |
| 🎨 **Watercolor** | Soft, painted | Artistic comics |
| 📰 **Vintage** | Muted, halftone | Retro comics |

---

## 🌐 Languages

| Code | Language |
|------|----------|
| `en` | English |
| `es` | Spanish |
| `fr` | French |
| `de` | German |
| `it` | Italian |
| `pt` | Portuguese |
| `ja` | Japanese |
| `zh` | Chinese |
| `ar` | Arabic |

---

## 🎯 Examples

### Example 1: Mouse on Road
**Prompt:** `mouse on road`

**Generated Story:**
> "Montgomery the mouse spots cheese across a busy road..."

**Result:** 4 panels showing the adventure with speech bubbles

### Example 2: Dragon Pizza
**Prompt:** `dragon eating pizza`

**Generated Story:**
> "Draco the dragon discovers his love for pepperoni..."

**Result:** Funny panels of a dragon struggling with pizza

### Example 3: Cat Astronaut
**Prompt:** `cat astronaut on moon`

**Generated Story:**
> "Whiskers becomes the first feline on the lunar surface..."

**Result:** Space-themed cat adventure

---

## 🔧 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| **"Failed to generate story"** | Check API key, internet connection |
| **Images not appearing** | Check `static/comics/` folder permissions |
| **Voice not working** | Allow microphone access in browser |
| **Upload fails** | File size < 5MB, valid image format |
| **Slow generation** | Normal for first request (cold start) |
| **Bubbles not showing** | Check panel number, refresh page |

### Browser Support

| Browser | Voice Support | Best Experience |
|---------|---------------|-----------------|
| **Chrome** | ✅ Full | ✅ Recommended |
| **Edge** | ✅ Full | ✅ Good |
| **Firefox** | ⚠️ Limited | ⚠️ Basic |
| **Safari** | ⚠️ Limited | ⚠️ Basic |

### Error Messages

| Error | Meaning | Fix |
|-------|---------|-----|
| `400 Bad Request` | Missing required field | Check your input |
| `404 Not Found` | Endpoint incorrect | Verify URL |
| `500 Server Error` | Server issue | Check logs, retry |
| `API key invalid` | Gemini key wrong | Update `.env` |

---

## 📝 Quick Reference Card

```bash
# Generate story
curl -X POST http://localhost:8080/generate-story -d '{"topic":"mouse"}'

# Generate comic
curl -X POST http://localhost:8080/generate-pages-with-characters -d '{"prompt":"mouse"}'

# Add bubble
curl -X POST http://localhost:8080/add-bubble -d '{"text":"Hello!"}'

# Download PDF
curl -X POST http://localhost:8080/download-pdf -d '{"pages":[...]}' --output comic.pdf

# Upload character
curl -X POST http://localhost:8080/api/upload-character -F "file=@image.jpg"
```

---

## 🎨 **Happy Comic Creating!**

For more help, check:
- [API Documentation](api.md)
- [Architecture Guide](architecture.md)
- [Deployment Guide](deployment.md)
- [GitHub Issues](https://github.com/RobinaMirbahar/Comic-Studio-Ai/issues)

---

*Last updated: March 9, 2026 • Version 2.0.0*
