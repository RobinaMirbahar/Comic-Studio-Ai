
# 📖 Comic Studio AI - Usage Guide

## 📋 Table of Contents
- [Quick Start](#quick-start)
- [🎨 Your First Comic - Visual Guide](#-your-first-comic---visual-guide)
- [Web Interface Guide](#web-interface-guide)
- [Conversational Agent](#conversational-agent)
- [Style Selection](#style-selection)
- [Panel Count & Random Prompt](#panel-count--random-prompt)
- [Image Generation](#image-generation)
- [Download Options](#download-options)
- [API Usage Guide](#api-usage-guide)
- [Art Styles](#art-styles)
- [Languages](#languages)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [📷 Adding Images to this Guide](#-adding-images-to-this-guide)

---

## 🚀 Quick Start

### 1. **Start the Server**

```bash
# Make sure you're in the project directory
cd Comic-Studio-Ai

# Create and activate virtual environment (if not already done)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all required dependencies
pip install fastapi uvicorn python-dotenv google-generativeai Pillow reportlab jinja2

# Run the app
python main.py
```

### 2. **Open in Browser**
```
http://localhost:8080
```

![Run the App](images/Run-the-App.jpg)

---

## 🎨 Your First Comic - Visual Guide

### Step 1: Enter a Prompt & Adjust Settings
Type your idea in the text area, choose language, and select number of panels (1–6). Example: **"penguin in a desert"**

```
┌─────────────────────────────────────┐
│ Language: [English ▼]               │
│ [penguin in a desert]       [🎲]    │
│ Panels: [=====○=====] (4)           │
│ [1. Generate Story]                  │
└─────────────────────────────────────┘
```
![Enter the prompt](images/enter-the-prompt.jpg)

### 🎤 Voice Input
- Click the **🎤 microphone button** next to the prompt field.
- Your browser will ask for microphone permission – allow it.
- Speak your comic idea clearly (e.g., "a cat in a spaceship").
- The spoken text will automatically fill the prompt box.
- Works best in Chrome, Edge, or Safari.

![Voice input button](images/audio.jpg)

## 📷 Upload Image Feature

You can upload a character image to make the comic feature a specific person or drawing. The AI will use it as a reference for the main character across all panels.

### How to Use
1. **Select an image** – Click the file input in the **"Upload a character image"** section.
   - Supported formats: JPEG, PNG (max 5MB).
   - A preview thumbnail will appear.

2. **Enter a prompt** – Describe the scene you want (e.g., `"a day at the beach"`).

3. **Generate story with image** – Click the purple **"📷 Generate Story with Image"** button (not the regular story button).

4. **Review the story** – The AI will describe your character based on the image and place them in the scene.

5. **Proceed normally** – Continue with the conversational agent, style selection, panel generation, and image creation.

### Tips
- Use clear, front‑facing images for best results.
- The character will look like your image in all four panels.
- Works great for photos, avatars, or even drawings.

![Upload preview](images/upload-image.jpg)

![Story with own image](images/storyownimage.jpg)

![Final comic with own character](images/own-imagecomic.jpg)
![Own image step 1](https://raw.githubusercontent.com/RobinaMirbahar/Comic-Studio-Ai/main/docs/images/01-ownimage.png)
![Own image step 2](https://raw.githubusercontent.com/RobinaMirbahar/Comic-Studio-Ai/main/docs/images/o2-ownimage.png)
![Own image step 3](https://raw.githubusercontent.com/RobinaMirbahar/Comic-Studio-Ai/main/docs/images/03-ownimage.png)


### Step 2: Generate Story
Click **"1. Generate Story"** – you'll see the AI-generated story with title, characters, and plot.

```
┌─────────────────────────────────────┐
│ 📖 Generated Story                   │
│ Desert Penguin Adventure             │
│ Characters:                          │
│ • Pingu – A lost penguin             │
│ • Cactus Carl – A grumpy cactus      │
│ Plot:                                 │
│ 1. Pingu wakes up in the desert...   │
│ 2. He asks Cactus Carl for water...  │
│ 3. Carl points to an oasis...        │
│ 4. Pingu finds water and friends.    │
└─────────────────────────────────────┘
```

![Generating Story](images/generating-story.jpg)
![Generated Story](images/generatedstroy.jpg)

### Step 3: Chat with the Conversational Agent
The agent appears and asks if you're satisfied. You can request changes like:
- `"add a dog character"`
- `"make the penguin braver"`
- `"change the ending to be funnier"`

  ![Add a dog character](images/add-a-dog.jpg)
  ![Make the penguin brave](images/makethepenguine-brave.jpg)
  ![Make it funnier](images/funier.jpg)
  ![Refining story](images/refiningstory.jpg)

Type your request, or simply say **"yes"** to proceed.
![Proceed to yes](images/proceesd-to-yes.jpg)

```
┌─────────────────────────────────────┐
│ 🎬 I've created a story. You can ask │
│    to change it, e.g., "add a dog".  │
│ 👤 add a dog                         │
│ 🎬 ⏳ Modifying...                    │
│ 🎬 Story updated!                     │
└─────────────────────────────────────┘
```
![Created story](images/createdstory.jpg)

### Step 4: Choose Your Style
After approving, select art style, language tone, and optional color palette.

```
┌─────────────────────────────────────┐
│ Art Style: [Manga ▼]                 │
│ Language Tone: [Adventurous ▼]       │
│ Color Palette: [warm]                 │
│ [2. Generate Panels]                  │
└─────────────────────────────────────┘
```
![Style selection](images/style.jpg)
![Language tone selection](images/tone.jpg)

### Step 5: Generate Panels & Dialogue
Click **"2. Generate Panels"** – the app creates 4 panel descriptions with dialogue and bubble types.

```
┌─────────────────────────────────────┐
│ Panel 1: Wide desert shot, Pingu...  │
│ Characters: Pingu                     │
│ Dialogue: "Where's the water?"        │
│ (speech)                              │
│ Panel 2: Pingu meets Cactus Carl...   │
│ ...                                   │
└─────────────────────────────────────┘
```
![Generated panels](images/panelgenerated.jpg)
![Panel generate](images/panelgenete.jpg)

### Step 6: Generate Images
Click **"3. Generate Images"** – the app uses Imagen to create actual comic panels (may take 10–20 seconds).

```
┌─────────────────────────────────────┐
│ [Image of Panel 1]                   │
│ ✓ Real Imagen generation             │
│ [Image of Panel 2]                   │
│ ...                                   │
└─────────────────────────────────────┘
```
![Images Generated](images/imagesgenerated.jpg)
![Generate Images Button](images/generateimages.jpg)
![Panel 1](images/01.png)
![Panel 2](images/02.png)
![Panel 3](images/03.png)
![Panel 4](images/04.png)

### Step 7: Download Your Comic
Choose **PDF** (one panel per page) or **Booklet** (two panels per page, landscape). Files include the story title and a timestamp.

```
┌─────────────────────────────────────┐
│ [PDF]    [Booklet]                   │
│ comic_PenguinAdventure_12345678.pdf  │
└─────────────────────────────────────┘
```
![Download buttons](images/download-buttons.jpg) *(replace with actual screenshot if available)*

### 📸 Example Gallery

#### Example 1: "cat in a hospital" (Spanish, humorous)
| Panel 1 | Panel 2 | Panel 3 | Panel 4 |
|---------|---------|---------|---------|
| Cat enters hospital | Meets a dog nurse | Gets a checkup | Makes friends |
*(Insert collage image here)*

#### Example 2: "robot on Mars" (English, adventurous)
| Panel 1 | Panel 2 | Panel 3 | Panel 4 |
|---------|---------|---------|---------|
| Robot lands | Explores crater | Finds alien | Sends message |
*(Insert collage image here)*

#### Example 3: "dragon at school" (Japanese, heartwarming)
| Panel 1 | Panel 2 | Panel 3 | Panel 4 |
|---------|---------|---------|---------|
| Dragon is nervous | Meets a friendly owl | Learns to breathe fire | Graduates |
*(Insert collage image here)*

### 🎯 Visual Workflow

```mermaid
graph TD
    A[Enter Prompt] --> B[Generate Story]
    B --> C{Conversational Agent}
    C -->|"Request changes"| B
    C -->|"Approve (yes)"| D[Choose Style]
    D --> E[Generate Panels]
    E --> F[Generate Images]
    F --> G[Download PDF/Booklet]
```

---

## 🖥️ Web Interface Guide

### Main Interface Sections

```
┌─────────────────────────────────────────────┐
│  HEADER & AGENT SHOWCASE                    │
│  (Researcher, Script Director, etc.)        │
├─────────────────────────────────────────────┤
│  LANGUAGE SELECTOR                           │
│  [English ▼]                                 │
├─────────────────────────────────────────────┤
│  PROMPT INPUT & VOICE/RANDOM BUTTONS         │
│  [penguin in a desert]   [🎤] [🎲]          │
├─────────────────────────────────────────────┤
│  IMAGE UPLOAD SECTION                        │
│  [Choose file] (preview)                     │
├─────────────────────────────────────────────┤
│  PANEL COUNT SLIDER                           │
│  [=====○=====] (4)                           │
│  [1. Generate Story] [📷 Gen. with Image]    │
├─────────────────────────────────────────────┤
│  STORY OUTPUT                                │
├─────────────────────────────────────────────┤
│  CONVERSATIONAL AGENT CHAT                    │
├─────────────────────────────────────────────┤
│  STYLE SELECTION                              │
├─────────────────────────────────────────────┤
│  PANELS & DIALOGUE OUTPUT                     │
├─────────────────────────────────────────────┤
│  IMAGE GENERATION & DOWNLOAD BUTTONS          │
│  [3. Generate Images] [PDF] [Booklet]       │
└─────────────────────────────────────────────┘
```
![Full interface](images/full-interface.jpg) *(replace with actual screenshot if available)*

### Agent Tooltips
Hover over any agent card to see its role.

![Agent tooltip](https://raw.githubusercontent.com/RobinaMirbahar/Comic-Studio-Ai/main/docs/images/tooltip.jpg)

---

## 💬 Conversational Agent

After story generation, the agent appears in a chat box. It helps you refine the story.

**How to use:**
- Type natural language requests like:
  - `"add a dog character"`
  - `"make the plot more adventurous"`
  - `"change the main character's name to Fluffy"`
  - `"make the ending happier"`
- The agent preserves existing characters and only adds/modifies as you ask.
- Say `"yes"` when you're satisfied to move to style selection.

**Example conversation:**
```
🎬 I've created a story. You can ask me to change it, e.g.:
   - 'add a dog character'
   - 'make the plot more adventurous'
   Just tell me, or say 'yes' to proceed.
👤 add a cat and a dog
🎬 ⏳ Modifying story...
🎬 Story updated! You can keep refining or say 'yes'.
👤 yes
🎬 Great! Now choose your style preferences and click "Generate Panels".
```
![Chat box](images/chat-box.jpg) *(replace with actual screenshot if available)*

---

## 🎨 Style Selection

Once you approve the story, you can choose:

- **Art Style** – Manga, Western, Anime, Watercolor, Sketch, Vintage, Cartoon
- **Language Tone** – Humorous, Dramatic, Sarcastic, Heartwarming, Adventurous, Mysterious
- **Color Palette** – Optional hint (e.g., "warm", "pastel", "dark")

If left blank, the AI decides.

![Style dropdowns](images/style-dropdowns.jpg) *(replace with actual screenshot if available)*

---

## 🔢 Panel Count & Random Prompt

### Panel Count Slider
Adjust the number of panels from 1 to 6. The story adapts.

![Panel slider](images/panel-slider.jpg) *(replace with actual screenshot if available)*

### Random Prompt Button (🎲)
Click the dice icon to get a random creative idea.

![Random prompt](images/random-prompt.jpg) *(replace with actual screenshot if available)*

---

## ✨ Image Generation

After generating panels, click **"3. Generate Images"** to create actual comic panels using Imagen (via `gemini-3.1-flash-image-preview`). This may take 10–20 seconds for four panels. Images appear as base64-encoded PNGs. If generation fails, a styled placeholder appears.

![Generated images with success message](images/imagesgenerated.jpg)

---

## 📥 Download Options

- **PDF** – Standard portrait PDF, one panel per page, with a title page showing style advice.
- **Booklet** – Landscape PDF, two panels per page, suitable for printing.

Filenames include the story title and a timestamp (e.g., `PenguinAdventure_12345678.pdf`).

![Download buttons](images/download-buttons.jpg) *(replace with actual screenshot if available)*

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
  -d '{"topic": "penguin in a desert", "language": "en", "panels": 4}'
```
![Curl example](images/curl-story.jpg) *(replace with actual screenshot if available)*

### 2. **Generate Story with Image**
```bash
curl -X POST http://localhost:8080/generate-story-with-image \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "penguin in a desert",
    "language": "en",
    "panels": 4,
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
  }'
```

### 3. **Refine Story**
```bash
curl -X POST http://localhost:8080/refine-story \
  -H "Content-Type: application/json" \
  -d '{
    "story": {...},
    "modification": "add a dog character",
    "language": "en"
  }'
```
![Refine story curl](images/curl-refine.jpg) *(replace with actual screenshot if available)*

### 4. **Generate Panels**
```bash
curl -X POST http://localhost:8080/generate-panels \
  -H "Content-Type: application/json" \
  -d '{
    "story": {...},
    "style": {"overall_style": "manga", "language_tone": "humorous"},
    "language": "en"
  }'
```
![Generate panels curl](images/curl-panels.jpg) *(replace with actual screenshot if available)*

### 5. **Generate Images**
```bash
curl -X POST http://localhost:8080/generate-images \
  -H "Content-Type: application/json" \
  -d '{
    "panels": [...],
    "style": {...},
    "dialogues": [...],
    "language": "en"
  }'
```
![Generate images curl](images/curl-images.jpg) *(replace with actual screenshot if available)*

### 6. **Download PDF**
```bash
curl -X POST http://localhost:8080/download-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "images": [...],
    "style_advice": {...},
    "story_title": "Penguin Adventure"
  }' \
  --output comic.pdf
```

### 7. **Download Booklet**
```bash
curl -X POST http://localhost:8080/download-booklet \
  -H "Content-Type: application/json" \
  -d '{
    "images": [...],
    "style_advice": {...},
    "story_title": "Penguin Adventure"
  }' \
  --output booklet.pdf
```

---

## 🎨 Art Styles

| Style | Description |
|-------|-------------|
| 🇯🇵 **Manga** | Black and white, screentones, speed lines |
| 🇺🇸 **Western** | Bold outlines, vibrant colors, superhero |
| ✨ **Anime** | Vibrant colors, glossy eyes, cel-shaded |
| ✏️ **Sketch** | Pencil sketch, rough lines, hand-drawn |
| 🎨 **Watercolor** | Soft gradients, painted look |
| 📰 **Vintage** | 1950s style, muted colors, halftone dots |
| 🎭 **Cartoon** | Looney Tunes style, exaggerated expressions |

![Art styles collage](images/art-styles.jpg) *(replace with actual screenshot if available)*

---

## 🌐 Languages

| Code | Language | RTL |
|------|----------|-----|
| `en` | English | no |
| `fr` | French | no |
| `es` | Spanish | no |
| `de` | German | no |
| `ja` | Japanese | no |
| `ar` | Arabic | yes |
| `ur` | Urdu | yes |

RTL layout is automatically applied for Arabic and Urdu.

![Language dropdown](images/language-dropdown.jpg) *(replace with actual screenshot if available)*
![RTL interface](images/rtl-arabic.jpg) *(replace with actual screenshot if available)*

---

## 🎯 Examples

### Example 1: "cat in a hospital"
**Language:** English  
**Panels:** 4  
**Style:** Cartoon, Heartwarming  
**Output:** A story about a lost cat who brings joy to patients.
*(Insert four panels collage)*

### Example 2: "robot on Mars" (French)
**Language:** French  
**Panels:** 6  
**Style:** Manga, Adventurous  
**Output:** A 6-panel comic about a robot exploring Mars.
*(Insert six panels collage)*

### Example 3: "penguin in a desert" (Urdu)
**Language:** Urdu  
**Panels:** 4  
**Style:** Watercolor, Mysterious  
**Output:** A beautifully illustrated story of a penguin seeking water.
*(Insert four panels collage)*

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| **"Failed to generate story"** | Check API key, internet connection. |
| **Image upload doesn't work** | Ensure file is under 5MB and is JPEG/PNG. |
| **Image generation fails** | Ensure your API key has access to `gemini-3.1-flash-image-preview`. Check logs. |
| **PDF download doesn't work** | Generate images first; try again. |
| **Conversational agent not adding characters** | Use precise requests like "add a dog character". The agent preserves existing ones. |
| **Slow performance** | First request may be slow due to cold start. Subsequent requests are faster. |
| **Arabic/Urdu text not RTL** | Ensure language is set correctly; the UI will switch automatically. |

![Error message](images/error.jpg) *(replace with actual screenshot if available)*

---

## 📷 Adding Images to this Guide

To insert images in this Markdown file, follow these steps:

1. **Create an `images` folder** inside `docs/`:
   ```bash
   mkdir -p docs/images
   ```
2. **Take screenshots** of your app.
3. **Save them** in `docs/images/` with descriptive names.
4. **Insert** using `![Alt text](images/filename.jpg)`.

---

## 🎨 **Happy Comic Creating!**

For more help, check:
- [API Documentation](api.md)
- [Architecture Guide](architecture.md)
- [Deployment Guide](deployment.md)
- [GitHub Issues](https://github.com/RobinaMirbahar/Comic-Studio-Ai/issues)

![Footer](images/footer.jpg) *(replace with actual screenshot if available)*

---

*Last updated: March 2026 • Version 2.0.0*
```
