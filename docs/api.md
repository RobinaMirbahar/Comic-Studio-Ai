
# 📡 API Documentation

## Base URL

When running locally:
```
http://localhost:8080
```

When deployed on Google Cloud Run:
```
https://comic-studio-ai-xyz-uc.a.run.app
```

## 🔐 Authentication

This API uses a Gemini API key configured via environment variable (`GEMINI_API_KEY`). No additional authentication is required for the public demo endpoints.

---

## 📋 Endpoints Overview

| Method | Endpoint                     | Description |
|--------|------------------------------|-------------|
| POST   | `/generate-story`            | Creates a comic story from a text prompt |
| POST   | `/generate-story-with-image` | Creates a story using a character image as reference |
| POST   | `/refine-story`              | Modifies an existing story based on user feedback |
| POST   | `/generate-panels`           | Generates panel descriptions and dialogue from a story |
| POST   | `/generate-images`           | Creates actual comic panel images using Imagen |
| POST   | `/download-pdf`              | Downloads all panels as a PDF document |
| POST   | `/download-booklet`          | Downloads panels as a booklet‑style PDF (two per page) |

---

## 🎯 Story Generation (Text Only)

### `POST /generate-story`

Generates a complete comic story with characters and plot from a user prompt.

**Request Body:**

```json
{
    "topic": "mouse on road",
    "language": "en",
    "panels": 4
}
```

| Field    | Type   | Required | Description |
|----------|--------|----------|-------------|
| `topic`  | string | ✅ Yes   | The story idea/prompt (min. 3 characters) |
| `language` | string | ❌ No   | Language code (default: `"en"`) |
| `panels` | integer| ❌ No   | Number of panels (1‑6, default: 4) |

**Supported Languages:**

| Code | Language   | RTL |
|------|------------|-----|
| en   | English    | no  |
| fr   | French     | no  |
| es   | Spanish    | no  |
| de   | German     | no  |
| ja   | Japanese   | no  |
| ar   | Arabic     | yes |
| ur   | Urdu       | yes |

**Success Response (200 OK):**

```json
{
    "title": "Mouse on Road: A Cheese-Lover's Crosswalk Catastrophe",
    "characters": [
        "Montgomery – A small, adventurous mouse with a weakness for sharp cheddar",
        "Bertha – A grumpy, overly cautious snail"
    ],
    "plot": [
        "Montgomery spots a giant block of cheddar on the other side of a busy road.",
        "He excitedly rushes forward, ignoring traffic, dreaming of cheesy paradise.",
        "A tiny car miraculously avoids him, but he grabs a cheddar crumb.",
        "Bertha scolds him as he blissfully nibbles his reward, declaring it 'totally worth it!'"
    ]
}
```

**Error Response (400 Bad Request):**

```json
{
    "error": "Topic required"
}
```

**Example using `curl`:**

```bash
curl -X POST http://localhost:8080/generate-story \
  -H "Content-Type: application/json" \
  -d '{"topic": "mouse on road", "language": "en", "panels": 4}'
```

---

## 🖼️ Story Generation with Image

### `POST /generate-story-with-image`

Generates a comic story where the **main character is based on a provided image**. The AI will describe the character and feature it in the story across all panels.

**Request Body:**

```json
{
    "topic": "a day at the beach",
    "language": "en",
    "panels": 4,
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
}
```

| Field    | Type   | Required | Description |
|----------|--------|----------|-------------|
| `topic`  | string | ✅ Yes   | The story idea/prompt |
| `language` | string | ❌ No   | Language code |
| `panels` | integer| ❌ No   | Number of panels (1‑6) |
| `image`  | string | ✅ Yes   | Base64‑encoded image (JPEG/PNG, max 5MB) |

**Success Response (200 OK):**

Same format as `/generate-story`, but the main character description will match the uploaded image.

**Example using `curl`:**

```bash
curl -X POST http://localhost:8080/generate-story-with-image \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "a day at the beach",
    "language": "en",
    "panels": 4,
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
  }'
```

---

## 💬 Story Refinement (Conversational Agent)

### `POST /refine-story`

Modifies an existing story according to natural language feedback. Preserves existing characters and only adds/removes as requested.

**Request Body:**

```json
{
    "story": {
        "title": "Mouse Adventure",
        "characters": ["Montgomery – ...", "Bertha – ..."],
        "plot": ["Panel 1...", "Panel 2...", "Panel 3...", "Panel 4..."]
    },
    "modification": "add a dog character",
    "language": "en"
}
```

| Field          | Type   | Required | Description |
|----------------|--------|----------|-------------|
| `story`        | object | ✅ Yes   | The story object from `/generate-story` or `/generate-story-with-image` |
| `modification` | string | ✅ Yes   | Natural language change request |
| `language`     | string | ❌ No   | Language code (must match original) |

**Success Response (200 OK):**

Returns the modified story in the same format.

**Example using `curl`:**

```bash
curl -X POST http://localhost:8080/refine-story \
  -H "Content-Type: application/json" \
  -d '{
    "story": {...},
    "modification": "make the mouse more curious",
    "language": "en"
  }'
```

---

## 🖼️ Panel & Dialogue Generation

### `POST /generate-panels`

Creates detailed panel descriptions and dialogue (with bubble types) from an approved story, incorporating user‑selected style preferences.

**Request Body:**

```json
{
    "story": { ... },
    "style": {
        "overall_style": "manga",
        "language_tone": "humorous",
        "color_palette": "vibrant"
    },
    "language": "en"
}
```

| Field            | Type   | Required | Description |
|------------------|--------|----------|-------------|
| `story`          | object | ✅ Yes   | The story object |
| `style`          | object | ❌ No   | Style preferences (see below) |
| `language`       | string | ❌ No   | Language code |

**Style object fields:**

| Field           | Type   | Description |
|-----------------|--------|-------------|
| `overall_style` | string | Art style (manga, western, anime, watercolor, sketch, vintage, cartoon) |
| `language_tone` | string | Tone of dialogue (humorous, dramatic, sarcastic, heartwarming, adventurous, mysterious) |
| `color_palette` | string | Optional color hint (e.g., "warm", "pastel", "dark") |

**Success Response (200 OK):**

```json
{
    "panels": [
        {
            "panel_number": 1,
            "description": "A wide shot of a desert...",
            "characters_present": ["Montgomery"],
            "suggested_art_style": "manga"
        },
        ...
    ],
    "dialogues": [
        {
            "panel_number": 1,
            "dialogues": [
                { "character": "Montgomery", "text": "I must cross!", "bubble_type": "speech" }
            ]
        },
        ...
    ],
    "style_advice": {
        "overall_style": "manga",
        "language_tone": "humorous",
        "color_palette": "vibrant"
    }
}
```

---

## 🎨 Image Generation (Imagen)

### `POST /generate-images`

Uses the `gemini-3.1-flash-image-preview` model to generate actual comic panel images based on the descriptions and dialogues. Images are returned as base64‑encoded PNGs.

**Request Body:**

```json
{
    "panels": [...],
    "style": { ... },
    "dialogues": [...],
    "language": "en"
}
```

**Success Response (200 OK):**

```json
{
    "images": [
        {
            "panel_number": 1,
            "image": "base64_encoded_image_data...",
            "description": "A wide shot of a desert..."
        },
        ...
    ]
}
```

If image generation fails, the `image` field will be `null`.

---

## 📥 PDF Download

### `POST /download-pdf`

Generates a PDF containing all comic panels (one per page) with a title page showing style advice.

**Request Body:**

```json
{
    "images": [...],
    "style_advice": { ... },
    "story_title": "Mouse Adventure"
}
```

| Field          | Type    | Required | Description |
|----------------|---------|----------|-------------|
| `images`       | array   | ✅ Yes   | Array of image objects from `/generate-images` |
| `style_advice` | object  | ✅ Yes   | Style advice object |
| `story_title`  | string  | ✅ Yes   | Title of the comic |

**Response:** PDF file download with filename `comic.pdf`.

---

### `POST /download-booklet`

Generates a booklet‑style PDF with two panels per page (landscape orientation), suitable for printing.

**Request Body:** Same as `/download-pdf`.

**Response:** PDF file download with filename `comic_booklet.pdf`.

---

## 🏥 Health Check

### `GET /health`

Verifies the API is running.

**Success Response (200 OK):**

```json
{
    "status": "healthy"
}
```

---

## ⚠️ Common Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 OK      | Request successful |
| 400 Bad Request | Invalid input (missing fields, wrong format) |
| 500 Internal Server Error | Server‑side error (check logs for details) |

---

## 💡 Tips for Developers

- Use the conversational agent (`/refine-story`) to iterate on the story – the agent understands natural language and preserves existing characters.
- Style preferences are optional; the AI will decide if left empty.
- Image generation may take 10‑20 seconds for four panels.
- PDF and booklet downloads include the story title and a timestamp in the filename for uniqueness.

---

## 📚 Example Workflow

```bash
# 1. Generate a story from text
curl -X POST http://localhost:8080/generate-story \
  -H "Content-Type: application/json" \
  -d '{"topic": "mouse on road", "language": "en", "panels": 4}' > story.json

# 2. (Optional) Generate a story from an image
curl -X POST http://localhost:8080/generate-story-with-image \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "a day at the beach",
    "language": "en",
    "panels": 4,
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
  }' > image-story.json

# 3. Refine the story
curl -X POST http://localhost:8080/refine-story \
  -H "Content-Type: application/json" \
  -d '{"story": '"$(cat story.json)"', "modification": "add a dog character"}' > refined.json

# 4. Generate panels
curl -X POST http://localhost:8080/generate-panels \
  -H "Content-Type: application/json" \
  -d '{"story": '"$(cat refined.json)"', "style": {"overall_style": "manga"}, "language": "en"}' > panels.json

# 5. Generate images
curl -X POST http://localhost:8080/generate-images \
  -H "Content-Type: application/json" \
  -d @panels.json > images.json

# 6. Download PDF
curl -X POST http://localhost:8080/download-pdf \
  -H "Content-Type: application/json" \
  -d '{"images": '"$(jq '.images' images.json)"', "style_advice": '"$(jq '.style_advice' panels.json)"', "story_title": "Mouse Adventure"}' \
  --output comic.pdf
```

---

## 📝 Notes

- All timestamps in responses are Unix epoch format.
- Image URLs are relative to the server root when stored locally; for generated images, they are returned as base64 data.
- Maximum request size is limited by the server configuration (default 10 MB).

Happy creating! 🎨
```
