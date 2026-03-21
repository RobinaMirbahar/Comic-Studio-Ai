# 📡 API Documentation

## Base URL

```
# Local
http://localhost:8080

# Google Cloud Run
https://comic-studio-ai-xyz-uc.a.run.app
```

## 🔐 Authentication

Configure your Gemini API key via the `GEMINI_API_KEY` environment variable. No additional authentication is required for public demo endpoints.

---

## 📋 Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| POST | `/generate-story` | Generate a comic story from a text prompt |
| POST | `/generate-story-with-image` | Generate a story using a character image as reference |
| POST | `/refine-story` | Modify an existing story based on natural language feedback |
| POST | `/generate-panels` | Generate panel descriptions and dialogue from a story |
| POST | `/generate-images` | Render comic panel images using Imagen |
| POST | `/download-pdf` | Download all panels as a PDF (one per page) |
| POST | `/download-booklet` | Download panels as a booklet PDF (two per page, landscape) |
| GET | `/health` | Verify the API is running |

---

## POST `/generate-story`

Generate a complete comic story — title, characters, and plot — from a text prompt.

**Request**

```json
{
  "topic": "mouse on road",
  "language": "en",
  "panels": 4
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `topic` | string | ✅ | Story idea or prompt (min. 3 characters) |
| `language` | string | — | Language code (default: `"en"`) |
| `panels` | integer | — | Number of panels, 1–6 (default: 4) |

**Supported Languages**

| Code | Language | RTL |
|---|---|---|
| `en` | English | — |
| `fr` | French | — |
| `es` | Spanish | — |
| `de` | German | — |
| `ja` | Japanese | — |
| `ar` | Arabic | ✓ |
| `ur` | Urdu | ✓ |

**Response — 200 OK**

```json
{
  "title": "Mouse on Road: A Cheese-Lover's Crosswalk Catastrophe",
  "characters": [
    "Montgomery – A small, adventurous mouse with a weakness for sharp cheddar",
    "Bertha – A grumpy, overly cautious snail"
  ],
  "plot": [
    "Montgomery spots a giant block of cheddar on the other side of a busy road.",
    "He rushes forward ignoring traffic, dreaming of cheesy paradise.",
    "A tiny car barely avoids him, but he grabs a cheddar crumb.",
    "Bertha scolds him as he blissfully nibbles his reward — 'totally worth it!'"
  ]
}
```

**Response — 400 Bad Request**

```json
{ "error": "Topic required" }
```

**Example**

```bash
curl -X POST http://localhost:8080/generate-story \
  -H "Content-Type: application/json" \
  -d '{"topic": "mouse on road", "language": "en", "panels": 4}'
```

---

## POST `/generate-story-with-image`

Generate a story where the main character is based on an uploaded image. The AI describes the character from the image and features them consistently across all panels.

**Request**

```json
{
  "topic": "a day at the beach",
  "language": "en",
  "panels": 4,
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `topic` | string | ✅ | Story idea or prompt |
| `language` | string | — | Language code |
| `panels` | integer | — | Number of panels, 1–6 |
| `image` | string | ✅ | Base64-encoded image (JPEG or PNG, max 5 MB) |

**Response — 200 OK**

Same format as `/generate-story`. The main character description will reflect the uploaded image.

**Example**

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

## POST `/refine-story`

Modify an existing story with a natural language instruction. Existing characters are preserved; only the requested changes are applied.

**Request**

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

| Field | Type | Required | Description |
|---|---|---|---|
| `story` | object | ✅ | Story object from `/generate-story` or `/generate-story-with-image` |
| `modification` | string | ✅ | Natural language change request |
| `language` | string | — | Language code — should match the original |

**Response — 200 OK**

Returns the modified story in the same format as `/generate-story`.

**Example**

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

## POST `/generate-panels`

Generate detailed panel descriptions and dialogue — including bubble types — from an approved story and style preferences.

**Request**

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

| Field | Type | Required | Description |
|---|---|---|---|
| `story` | object | ✅ | Story object |
| `style` | object | — | Style preferences (see below) |
| `language` | string | — | Language code |

**Style object**

| Field | Type | Options |
|---|---|---|
| `overall_style` | string | `manga`, `western`, `anime`, `watercolor`, `sketch`, `vintage`, `cartoon` |
| `language_tone` | string | `humorous`, `dramatic`, `sarcastic`, `heartwarming`, `adventurous`, `mysterious` |
| `color_palette` | string | Optional hint — e.g., `"warm"`, `"pastel"`, `"dark"` |

All style fields are optional; the AI will decide if omitted.

**Response — 200 OK**

```json
{
  "panels": [
    {
      "panel_number": 1,
      "description": "A wide shot of a desert...",
      "characters_present": ["Montgomery"],
      "suggested_art_style": "manga"
    }
  ],
  "dialogues": [
    {
      "panel_number": 1,
      "dialogues": [
        { "character": "Montgomery", "text": "I must cross!", "bubble_type": "speech" }
      ]
    }
  ],
  "style_advice": {
    "overall_style": "manga",
    "language_tone": "humorous",
    "color_palette": "vibrant"
  }
}
```

---

## POST `/generate-images`

Render actual comic panel images using `gemini-3.1-flash-image-preview` (Imagen). Images are returned as base64-encoded PNGs. Four panels typically take 10–20 seconds.

**Request**

```json
{
  "panels": [...],
  "style": { ... },
  "dialogues": [...],
  "language": "en"
}
```

**Response — 200 OK**

```json
{
  "images": [
    {
      "panel_number": 1,
      "image": "base64_encoded_image_data...",
      "description": "A wide shot of a desert..."
    }
  ]
}
```

If generation fails for a panel, its `image` field will be `null` and a styled placeholder is shown in the UI.

---

## POST `/download-pdf`

Generate a portrait PDF with one panel per page, including a title page with style advice.

**Request**

```json
{
  "images": [...],
  "style_advice": { ... },
  "story_title": "Mouse Adventure"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `images` | array | ✅ | Image objects from `/generate-images` |
| `style_advice` | object | ✅ | Style advice from `/generate-panels` |
| `story_title` | string | ✅ | Title used in the filename and title page |

**Response:** PDF file — `comic.pdf`

---

## POST `/download-booklet`

Generate a landscape booklet PDF with two panels per page, suitable for printing.

**Request:** Same as `/download-pdf`.

**Response:** PDF file — `comic_booklet.pdf`

---

## GET `/health`

Verify the API is running.

**Response — 200 OK**

```json
{ "status": "healthy" }
```

---

## ⚠️ Error Codes

| Code | Meaning |
|---|---|
| `200 OK` | Request successful |
| `400 Bad Request` | Invalid input — missing fields or wrong format |
| `500 Internal Server Error` | Server-side error — check logs for details |

---

## 📚 Full Workflow Example

```bash
# 1. Generate story
curl -X POST http://localhost:8080/generate-story \
  -H "Content-Type: application/json" \
  -d '{"topic": "mouse on road", "language": "en", "panels": 4}' \
  > story.json

# 2. Refine the story
curl -X POST http://localhost:8080/refine-story \
  -H "Content-Type: application/json" \
  -d '{"story": '"$(cat story.json)"', "modification": "add a dog character"}' \
  > refined.json

# 3. Generate panels
curl -X POST http://localhost:8080/generate-panels \
  -H "Content-Type: application/json" \
  -d '{"story": '"$(cat refined.json)"', "style": {"overall_style": "manga"}, "language": "en"}' \
  > panels.json

# 4. Generate images
curl -X POST http://localhost:8080/generate-images \
  -H "Content-Type: application/json" \
  -d @panels.json \
  > images.json

# 5. Download PDF
curl -X POST http://localhost:8080/download-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "images": '"$(jq '.images' images.json)"',
    "style_advice": '"$(jq '.style_advice' panels.json)"',
    "story_title": "Mouse Adventure"
  }' \
  --output comic.pdf
```

---

## 📝 Notes

- All style fields are optional — the AI will make sensible decisions when omitted.
- The conversational agent (`/refine-story`) understands natural language and preserves existing characters — iterate freely before generating panels.
- Image generation is the slowest step (~10–20s for 4 panels); plan accordingly in any integration.
- PDF filenames include the story title and a Unix timestamp for uniqueness.
- Maximum request size is 10 MB (server default).
- Base64 image data is returned directly in the response body; no separate asset hosting is required.
