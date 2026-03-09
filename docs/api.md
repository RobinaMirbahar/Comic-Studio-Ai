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

---

## 🔐 Authentication

This API uses Google Cloud Secret Manager for securing the Gemini API key. No additional authentication is required for the endpoints themselves as this is a public demo application.

---

## 📋 Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/generate-story` | Generates a comic story from a text prompt |
| `POST` | `/generate-pages-with-characters` | Creates 4 comic panels with consistent characters |
| `POST` | `/add-bubble` | Adds/edits speech bubbles on existing panels |
| `POST` | `/download-zip` | Downloads all panels as a ZIP archive |
| `POST` | `/download-pdf` | Downloads all panels as a PDF document |
| `POST` | `/download-booklet` | Downloads panels as a booklet-style PDF |
| `POST` | `/api/upload-character` | Uploads a custom character image |
| `GET` | `/api/characters` | Lists all uploaded characters |
| `DELETE` | `/api/characters/{char_id}` | Deletes a specific character |

---

## 🎯 Story Generation

### `POST /generate-story`

Generates a complete comic story with characters and plot from a user prompt.

**Request Body:**

```json
{
    "topic": "mouse on road",
    "language": "en"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `topic` | string | ✅ Yes | The story idea/prompt (min. 3 characters) |
| `language` | string | ❌ No | Language code (default: "en") |

**Supported Languages:**

| Code | Language |
|------|----------|
| `en` | English |
| `es` | Spanish |
| `fr` | French |
| `de` | German |
| `ja` | Japanese |
| `ar` | Arabic |

**Success Response (200 OK):**

```json
{
    "title": "Mouse on Road: A Cheese-Lover's Crosswalk Catastrophe",
    "characters": [
        "Montgomery - A small, adventurous mouse with a weakness for sharp cheddar",
        "Bertha - A grumpy, overly cautious snail"
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
  -d '{
    "topic": "mouse on road",
    "language": "en"
  }'
```

---

## 🖼️ Comic Panel Generation

### `POST /generate-pages-with-characters`

Generates 4 comic panels based on the story, with consistent characters and optional custom uploads.

**Request Body:**

```json
{
    "story": {
        "title": "Mouse on Road Adventure",
        "characters": ["Montgomery", "Bertha"],
        "plot": ["Scene 1", "Scene 2", "Scene 3", "Scene 4"]
    },
    "language": "en",
    "style": "manga",
    "panels": 4,
    "character_ids": ["char_abc123", "char_def456"],
    "prompt": "mouse on road"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `story` | object | ✅ Yes | Story object from `/generate-story` |
| `language` | string | ❌ No | Language code (default: "en") |
| `style` | string | ❌ No | Art style (see below) |
| `panels` | integer | ❌ No | Number of panels (default: 4) |
| `character_ids` | array | ❌ No | IDs of uploaded characters to include |
| `prompt` | string | ✅ Yes | Original user prompt |

**Supported Art Styles:**

| Style | Description |
|-------|-------------|
| `manga` | Japanese manga, black and white, screentones |
| `western` | American comic, bold colors, superhero style |
| `anime` | Japanese anime, vibrant colors, cel-shaded |
| `sketch` | Pencil sketch, rough lines, hand-drawn |
| `watercolor` | Soft gradients, painted look, artistic |
| `vintage` | 1950s style, muted colors, halftone dots |

**Success Response (200 OK):**

```json
[
    "/static/comics/page_1.png",
    "/static/comics/page_2.png",
    "/static/comics/page_3.png",
    "/static/comics/page_4.png"
]
```

**Error Response (500 Internal Server Error):**

```json
{
    "error": "Failed to generate comic pages"
}
```

**Example using `curl`:**

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

---

## 💬 Bubble Management

### `POST /add-bubble`

Adds or edits a speech bubble on an existing comic panel.

**Request Body:**

```json
{
    "image_url": "/static/comics/page_1.png",
    "text": "I need to cross this road!",
    "bubble_type": "speech",
    "emotion": "excited",
    "position": "bottom",
    "panel_index": 0
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image_url` | string | ✅ Yes | URL of the comic panel |
| `text` | string | ✅ Yes | Dialogue text |
| `bubble_type` | string | ❌ No | Type of bubble (see below) |
| `emotion` | string | ❌ No | Character emotion |
| `position` | string | ❌ No | Bubble position on panel |
| `panel_index` | integer | ❌ No | Panel number (0-3) |

**Bubble Types:**

| Type | Description |
|------|-------------|
| `speech` | Round white bubble with tail (default) |
| `thought` | Cloud-like bubble with circles |
| `shout` | Yellow bubble with red border, jagged edges |
| `whisper` | Dotted border, italic text |
| `narration` | Yellow box, serif font |
| `sfx` | Big red text, no bubble |

**Emotions:**

| Emotion | Effect |
|---------|--------|
| `neutral` | No emoji (default) |
| `happy` | Adds 😊 emoji |
| `sad` | Adds 😢 emoji |
| `angry` | Adds 😠 emoji |
| `excited` | Adds 🤩 emoji |
| `scared` | Adds 😨 emoji |

**Positions:**

| Position | Description |
|----------|-------------|
| `top` | Top center of panel |
| `bottom` | Bottom center of panel (default) |
| `left` | Left side, vertically centered |
| `right` | Right side, vertically centered |
| `auto` | AI chooses best position |

**Success Response (200 OK):**

```json
{
    "success": true,
    "new_image_url": "/static/comics/page_1_bubble.png",
    "message": "Added speech bubble"
}
```

**Error Response (500 Internal Server Error):**

```json
{
    "success": false,
    "error": "Failed to add bubble"
}
```

**Example using `curl`:**

```bash
curl -X POST http://localhost:8080/add-bubble \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "/static/comics/page_1.png",
    "text": "Here I go!",
    "bubble_type": "shout",
    "emotion": "excited",
    "position": "top"
  }'
```

---

## 📥 Download Endpoints

### `POST /download-zip`

Downloads all comic panels as a ZIP archive.

**Request Body:**

```json
{
    "pages": [
        "/static/comics/page_1.png",
        "/static/comics/page_2.png",
        "/static/comics/page_3.png",
        "/static/comics/page_4.png"
    ],
    "title": "My Comic Adventure"
}
```

**Response:** ZIP file download

**Example using `curl`:**

```bash
curl -X POST http://localhost:8080/download-zip \
  -H "Content-Type: application/json" \
  -d '{
    "pages": ["/static/comics/page_1.png", "/static/comics/page_2.png"],
    "title": "mouse_on_road"
  }' \
  --output comic.zip
```

---

### `POST /download-pdf`

Downloads all comic panels as a PDF document.

**Request Body:**

```json
{
    "pages": [
        "/static/comics/page_1.png",
        "/static/comics/page_2.png",
        "/static/comics/page_3.png",
        "/static/comics/page_4.png"
    ],
    "title": "My Comic Adventure",
    "language": "en"
}
```

**Response:** PDF file download

---

### `POST /download-booklet`

Downloads comic panels as a booklet-style PDF (2 pages per sheet for printing).

**Request Body:**

```json
{
    "pages": [
        "/static/comics/page_1.png",
        "/static/comics/page_2.png",
        "/static/comics/page_3.png",
        "/static/comics/page_4.png"
    ],
    "title": "My Comic Adventure"
}
```

**Response:** Booklet PDF download

---

## 👤 Character Management

### `POST /api/upload-character`

Uploads a custom character image for use in comics.

**Request (multipart/form-data):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | file | ✅ Yes | Image file (PNG, JPG, GIF, max 5MB) |

**Success Response (200 OK):**

```json
{
    "success": true,
    "id": "char_abc123",
    "url": "/static/uploads/char_abc123_1234567890.jpg",
    "thumb_url": "/static/uploads/thumb_char_abc123_1234567890.jpg"
}
```

**Error Response (400 Bad Request):**

```json
{
    "success": false,
    "error": "File too large (max 5MB)"
}
```

**Example using `curl`:**

```bash
curl -X POST http://localhost:8080/api/upload-character \
  -F "file=@/path/to/character.jpg"
```

---

### `GET /api/characters`

Returns a list of all uploaded characters.

**Success Response (200 OK):**

```json
{
    "characters": [
        {
            "id": "char_abc123",
            "filename": "char_abc123_1234567890.jpg",
            "thumbnail": "thumb_char_abc123_1234567890.jpg",
            "original_name": "my_character.jpg",
            "uploaded_at": 1709731200,
            "url": "/static/uploads/char_abc123_1234567890.jpg",
            "thumb_url": "/static/uploads/thumb_char_abc123_1234567890.jpg"
        }
    ]
}
```

---

### `DELETE /api/characters/{char_id}`

Deletes a specific uploaded character.

**Path Parameter:**
- `char_id`: The unique ID of the character (e.g., "char_abc123")

**Success Response (200 OK):**

```json
{
    "success": true
}
```

**Error Response (404 Not Found):**

```json
{
    "success": false,
    "error": "Character not found"
}
```

**Example using `curl`:**

```bash
curl -X DELETE http://localhost:8080/api/characters/char_abc123
```

---

## 🏥 Health Check

### `GET /health`

Verifies that the API is running.

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
| `200 OK` | Request successful |
| `400 Bad Request` | Invalid input (missing fields, wrong format) |
| `404 Not Found` | Resource not found |
| `500 Internal Server Error` | Server-side error (check logs) |

---

## 📊 Rate Limiting

Currently, no rate limits are enforced. However, please be mindful of Google Gemini API quotas.

---

## 💡 Tips for Developers

1. **Always include the original `prompt`** when generating comics for best results
2. **Character IDs are optional** - the AI will create characters if none are provided
3. **Bubble positioning** works best with `"auto"` for complex scenes
4. **Check the logs** for detailed error messages when things go wrong

---

## 📚 Example Workflow

```bash
# 1. Generate a story
curl -X POST http://localhost:8080/generate-story \
  -H "Content-Type: application/json" \
  -d '{"topic": "mouse on road"}' > story.json

# 2. Generate comic panels
curl -X POST http://localhost:8080/generate-pages-with-characters \
  -H "Content-Type: application/json" \
  -d '{
    "story": '"$(cat story.json)"',
    "style": "manga",
    "prompt": "mouse on road"
  }'

# 3. Download as PDF
curl -X POST http://localhost:8080/download-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "pages": ["/static/comics/page_1.png", "/static/comics/page_2.png", "/static/comics/page_3.png", "/static/comics/page_4.png"],
    "title": "Mouse Adventure"
  }' \
  --output comic.pdf
```

---

## 📝 Notes

- All timestamps are in Unix epoch format
- Image URLs are relative to the server root
- Maximum file size for uploads: 5MB
- Supported image formats: PNG, JPG, JPEG, GIF

---

**Happy coding! 🎨**
