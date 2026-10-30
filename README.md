# Hieroglyph Assistant (Kemet Studio)

This project is a FastAPI application for learning about and analyzing Ancient Egyptian hieroglyphs using Computer Vision and NLP. It has four main features:

- **AI Scribe Chat**: An expert Egyptologist conversational assistant powered by Groq LLM that explains hieroglyphic symbols, Gardiner codes, language, deities, and history—always providing authentic Unicode hieroglyphs (e.g., 𓋹, 𓀀, 𓇳). It answers fluently in both English and Arabic and is unlinked from rigid database limits.
- **Visual Detector**: An image-detection endpoint that uses a trained YOLOv11 model with zero-shot CLIP pre-filtering to localize and identify Gardiner signs in photos of inscriptions.
- **Symbol Explorer**: An interactive catalog of 179 curated hieroglyphic signs with phonetic values, categories, and English/Arabic narratives stored in `data/Semantic meaning.json`.
- **Voice Studio**: A neural speech synthesis service using Kokoro-82M to read aloud sign stories and custom hieroglyphic narratives in high-quality 24 kHz audio.

The Groq API key stays securely on the server in `.env`; it is never sent to the browser.

## Project structure

| Path | Purpose |
| --- | --- |
| `app.py` | Main FastAPI application connecting chat, vision detection, and speech endpoints. |
| `chatbot.py` | AI Scribe service: Groq LLM client, prompt engineering, request validation, and API routes. |
| `data/Semantic meaning.json` | Curated catalog data for 179 hieroglyph signs used in the Symbol Explorer and Audio Storyteller. |
| `models/best.pt` | Trained YOLOv11 hieroglyphic sign detection checkpoint. |
| `notebooks/` | Computer vision training and TTS experiment notebooks. |
| `tests/` | Automated pytest suite for API routes, integration, and chatbot services. |
| `requirements-chatbot.txt` | Python package dependencies for running the full studio pipeline. |
| `.env.example` | Example environment configuration file. |

## Start the application

Open PowerShell in the project folder and run:

```powershell
pip install -r requirements-chatbot.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Add your Groq key

The server can start without an API key, but the AI Scribe needs a Groq key to answer chat inquiries:

1. Copy `.env.example` to a new file named `.env`.
2. Open `.env` locally.
3. Replace `your_groq_api_key_here` with your key from Groq.
4. Restart the server.

Example:

```env
GROQ_API_KEY=your_real_key_here
GROQ_MODEL=openai/gpt-oss-20b
GLYPH_DATA_PATH=data/Semantic meaning.json
```

Do not commit `.env`. Git ignores it.

## Test the project

Run the automated test suite:

```powershell
python -m pytest -q
```

You can also check server health:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/health
```

Expected result: JSON with `"status": "API is running"` and `"story_records": 179`.

## Try the AI Scribe in the browser

Use these example queries after the server is running and your Groq key is configured:

| Input / Code | Question | Expected result |
| --- | --- | --- |
| `A1` | `What does A1 mean?` | Detailed breakdown of the seated man glyph (𓀀), its transliteration, determinative role, and meaning. |
| `S34` | `Explain this symbol in Arabic.` | Scholarly explanation of the Ankh (𓋹) and eternal life in Arabic with authentic hieroglyphs. |
| `𓀀` | `Tell me more about this sign.` | Full Egyptological explanation of the Unicode glyph 𓀀 and its Gardiner category. |
| Ra / Isis | `Who is the sun-god Ra and how is his name written?` | Historical narrative and name written in hieroglyphs (𓂋𓏏). |

You can enter known Gardiner codes or Unicode symbols in the **Active hieroglyphs & Gardiner codes** box, or upload an image. Manual codes remain useful when you already know the symbol or want to guide the conversation.

## Upload an image in the studio

Use the **Drop inscription image here** area or paste directly with `Ctrl+V`. The studio accepts JPG, PNG, and WebP images up to 10 MB.

After upload, the app:

1. Screens the image with zero-shot CLIP to ensure it contains hieroglyphic inscriptions.
2. Runs the trained YOLO detector when the screen passes.
3. Shows an annotated image with bounding boxes, Gardiner codes (e.g. `A1`), and confidence scores.
4. Automatically attaches detected codes to the AI Scribe for follow-up conversational questions.
5. Keeps symbol labels (e.g. `Symbol 1`, `Symbol 2`) for reference in chat.

Each chatbot answer includes a **Play audio** button to generate speech using the Kokoro neural voice synthesizer.

## Important notes

- Heavy computer vision and speech dependencies load lazily only when their respective endpoints are called, keeping startup fast.
- The AI Scribe draws upon broad Egyptological knowledge and embeds Unicode hieroglyphs in answers rather than restricting responses to local files.
- The curated catalog (`data/Semantic meaning.json`) serves as a structured reference for the Symbol Explorer and quick audio story generation.
