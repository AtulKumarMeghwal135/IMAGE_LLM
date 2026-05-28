# VisionLens — Multimodal LLM Demo
### MNIT Jaipur · Research Internship Project

---

## What this app does
Upload any image (JPG, PNG, WEBP, GIF, or iPhone HEIC photos) and ask questions about it.
The app uses Claude's multimodal API to analyze the image using vision + language together.

---

## How to run (IMPORTANT)

You CANNOT just double-click index.html — browsers block API calls from local files (CORS policy).
You must run it through a local server. Here are 3 easy ways:

---

### Option 1 — Python (Recommended, easiest)
If you have Python installed (check with `python --version`):

```
# In terminal / command prompt, navigate to this folder:
cd path/to/multimodal-analyzer

# Then run:
python start.py
```

The browser will open automatically at http://localhost:8000

---

### Option 2 — VS Code Live Server
1. Open the folder in VS Code
2. Install the "Live Server" extension (by Ritwick Dey)
3. Right-click index.html → "Open with Live Server"

---

### Option 3 — Node.js
```
npx serve .
```
Then open http://localhost:3000

---

## Getting an API Key
1. Go to https://console.anthropic.com
2. Sign up / log in
3. Click "API Keys" → "Create Key"
4. Paste it into the app's API Key field

Note: New accounts get free credits to start with.

---

## How Multimodal LLMs work (for your statement of interest)

1. **Vision Encoder** — The image is split into patches (e.g. 16x16 pixels each).
   Each patch is converted to a vector embedding using a Vision Transformer (ViT).

2. **Cross-modal Fusion** — The image embeddings and text token embeddings are
   projected into the same vector space and concatenated into one sequence.

3. **Language Generation** — The transformer decoder attends over both image and
   text tokens using self-attention, generating the answer token by token.

---

## Tech Stack
- HTML / CSS / Vanilla JS (no framework needed)
- Anthropic Claude API (claude-sonnet-4)
- heic2any library for iPhone photo conversion
- Python http.server for local hosting

---

Built for MNIT Jaipur CS Department — Multimodal LLM Research Internship Application
