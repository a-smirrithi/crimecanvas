# CrimeCanvas — AI Evidence Board

> Type a case name. AI builds your detective board in real time.

![CrimeCanvas](https://img.shields.io/badge/Gemini-2.0%20Flash-blue?style=flat-square&logo=google)
![Vercel](https://img.shields.io/badge/Deployed-Vercel-black?style=flat-square&logo=vercel)
![Hackathon](https://img.shields.io/badge/Gemini%20Live%20Agent%20Challenge-2026-red?style=flat-square)

---

## What is CrimeCanvas?

CrimeCanvas is an AI-powered detective evidence board. You type any criminal case name — historical cold case, true crime mystery, or unsolved disappearance — and the AI agent instantly:

- Extracts **suspects**, **evidence items**, **locations**, and **timeline events**
- Renders a fully interactive **cork board** with draggable cards pinned by type
- Draws **weighted red string connections** between related entities
- Shows a scrollable **timeline strip** at the bottom
- Surfaces **key investigative insights**
- Lets you **export** the full case as a JSON file

---

## Live Demo

🔗 **[crimecanvas.vercel.app](https://crimecanvas.vercel.app)**

---

## Screenshots

| Evidence Board | Timeline | Insights |
|---|---|---|
| Draggable cards with red string connections | Chronological event strip | AI-generated key insights panel |

---

## Hackathon Category

**UI Navigator ☸️** — Gemini Live Agent Challenge 2026

The agent interprets case descriptions, autonomously extracts structured visual entities, and generates an interactive spatial evidence board — going far beyond text-in/text-out interaction.

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Model | **Gemini 2.0 Flash** (google-generativeai SDK) |
| Backend | **Python** serverless function (Vercel) |
| Frontend | Vanilla HTML / CSS / JavaScript |
| Hosting | **Vercel** (frontend + backend) |
| Output Format | Structured JSON via `responseMimeType: application/json` |

---

## Architecture

```
User types case name
        │
        ▼
  Frontend (public/index.html)
  Vanilla JS — interactive SVG board
        │
        │  POST /api/investigate
        ▼
  Backend (api/investigate.py)
  Python serverless — Vercel function
        │
        │  google-generativeai SDK
        ▼
  Gemini 2.0 Flash
  Extracts: suspects / evidence /
  locations / timeline / connections
        │
        ▼
  Structured JSON response
        │
        ▼
  Frontend renders:
  ├── Draggable cards (suspects=red pin,
  │   evidence=yellow, locations=blue)
  ├── SVG red string connections
  ├── Timeline strip
  ├── Insights panel
  └── Export JSON
```

---

## Features

- **8 preset cases** — Jack the Ripper, D.B. Cooper, Zodiac Killer, Black Dahlia, Amelia Earhart, Lizzie Borden, JFK Assassination, Marilyn Monroe
- **Custom case input** — type any case name
- **Draggable cards** — rearrange the board freely
- **Scroll to zoom** — mouse wheel zooms in/out
- **Click to pan** — drag the background to explore
- **Red string connections** — weighted by relationship strength
- **Toggle strings** — hide/show all connections
- **Insights panel** — AI-generated key investigative insights
- **Timeline strip** — chronological events at the bottom
- **Sidebar entity list** — click any entity to focus it on board
- **Export JSON** — download the full case data
- **Touch support** — pinch to zoom, drag to pan on mobile

---

## Run Locally

### Prerequisites
- Python 3.11+
- A Gemini API key from [aistudio.google.com](https://aistudio.google.com)

### 1. Clone the repo
```bash
git clone https://github.com/a-smirrithi/crimecanvas.git
cd crimecanvas
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your API key
```bash
export GEMINI_API_KEY="your-key-here"
```

### 4. Run the backend
```bash
cd api
python -c "
import os, json
os.environ['GEMINI_API_KEY'] = os.environ.get('GEMINI_API_KEY','')
from http.server import HTTPServer
from investigate import handler
HTTPServer(('localhost', 8080), handler).serve_forever()
"
```

### 5. Open the frontend
Open `public/index.html` in your browser — or serve it:
```bash
python -m http.server 3000
# Visit http://localhost:3000/public/index.html
```

---

## Deploy to Vercel

### One-click deploy
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/a-smirrithi/crimecanvas)

### Manual deploy
```bash
npm i -g vercel
vercel --prod
```
Add environment variable `GEMINI_API_KEY` in Vercel dashboard → Settings → Environment Variables.

---

## Project Structure

```
crimecanvas/
├── README.md                 ← you are here
├── vercel.json               ← Vercel routing config
├── requirements.txt          ← Python dependencies
├── .gitignore
├── api/
│   └── investigate.py        ← Gemini 2.0 Flash backend
└── public/
    └── index.html            ← Full frontend app
```

---

## API Reference

### `POST /api/investigate`

**Request:**
```json
{
  "case_name": "Jack the Ripper murders 1888"
}
```

**Response:**
```json
{
  "data": {
    "case_title": "The Jack the Ripper Murders",
    "case_summary": "...",
    "suspects": [...],
    "evidence": [...],
    "locations": [...],
    "timeline": [...],
    "connections": [...],
    "insights": [...]
  }
}
```

### `GET /api/investigate`

Health check — returns `{"status": "ok", "model": "gemini-2.0-flash"}`

---

## Judging Criteria Coverage

### Innovation & Multimodal UX (40%)
- Breaks the text-box paradigm entirely — input is a case name, output is a spatial interactive board
- Visual + structural output: draggable cards, SVG string connections, timeline, insights
- Real-time board assembly feels like watching a detective work live

### Technical Implementation (30%)
- Gemini 2.0 Flash via `google-generativeai` SDK
- `responseMimeType: "application/json"` for reliable structured extraction
- Temperature 0.25 for factual, grounded responses
- Safety settings tuned for historical crime content
- Vercel serverless Python function — zero infrastructure overhead

### Demo & Presentation (30%)
- Live demo at crimecanvas.vercel.app
- Architecture diagram included above
- Real working software — no mockups

---

## Findings & Learnings

- **Gemini 2.0 Flash** is remarkably accurate at extracting structured entities from open-ended historical case descriptions — even obscure cold cases return rich, accurate data
- **`responseMimeType: "application/json"`** eliminates all JSON parsing failures — critical for reliable agentic pipelines
- The visual impact of the evidence board comes almost entirely from the SVG string layer — simple curved bezier paths create the "red string detective" aesthetic convincingly
- **Temperature 0.25** gives factual grounding without hallucination while still writing compelling descriptions

---

## Built By

**a-smirrithi** — built for the Gemini Live Agent Challenge 2026

*This project was created for the purposes of entering the Gemini Live Agent Challenge 2026 hackathon.*

**#GeminiLiveAgentChallenge**

---

## License

MIT
