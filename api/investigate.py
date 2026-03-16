import json, os, re
from http.server import BaseHTTPRequestHandler
import google.generativeai as genai

KEY   = os.environ.get("GEMINI_API_KEY", "AIzaSyDxQbps40t2Fvh-xrxzgcIeqcApzdXdd5g")
MODEL = "gemini-2.5-flash"

PROMPT = """Analyze this criminal case: "{name}"

You MUST return ONLY a valid JSON object. No extra text, no markdown, no code fences.

Return exactly this structure:
{{
  "case_title": "string",
  "case_summary": "string",
  "key_insight": "string",
  "suspects": [
    {{"id":"s1","name":"string","role":"string","description":"string","motive":"string","status":"string"}}
  ],
  "evidence": [
    {{"id":"e1","name":"string","type":"string","description":"string","found_at":"string"}}
  ],
  "locations": [
    {{"id":"l1","name":"string","significance":"string","events":"string"}}
  ],
  "timeline": [
    {{"id":"t1","date":"string","event":"string","detail":"string"}}
  ],
  "connections": [
    {{"from":"s1","to":"e1","label":"string","strength":"strong"}}
  ],
  "insights": ["string","string","string"]
}}

Rules:
- 3 suspects minimum
- 4 evidence items minimum
- 2 locations minimum
- 5 timeline events minimum
- 5 connections minimum
- strength must be: strong, moderate, or weak
- All from/to in connections must match valid ids above
- NO trailing commas
- NO single quotes
- ONLY double quotes in JSON
- Return raw JSON only, nothing else"""


def cors(h):
    h.send_header("Access-Control-Allow-Origin", "*")
    h.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    h.send_header("Access-Control-Allow-Headers", "Content-Type")

def send(h, status, data):
    body = json.dumps(data).encode()
    h.send_response(status)
    h.send_header("Content-Type", "application/json")
    h.send_header("Content-Length", str(len(body)))
    cors(h)
    h.end_headers()
    h.wfile.write(body)

def clean_json(text):
    text = text.strip()
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    text = text.strip()
    start = text.find('{')
    end   = text.rfind('}')
    if start != -1 and end != -1:
        text = text[start:end+1]
    text = re.sub(r',\s*}', '}', text)
    text = re.sub(r',\s*]', ']', text)
    return text


class handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_OPTIONS(self):
        self.send_response(204); cors(self); self.end_headers()

    def do_GET(self):
        send(self, 200, {"status": "ok", "model": MODEL})

    def do_POST(self):
        try:
            n    = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(n))
            name = body.get("case_name", "").strip()

            if not name:
                return send(self, 400, {"error": "case_name required"})

            genai.configure(api_key=KEY)
            model = genai.GenerativeModel(MODEL)

            response = model.generate_content(
                PROMPT.format(name=name),
                generation_config=genai.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=4000,
                    response_mime_type="application/json"
                ),
                safety_settings=[
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT",  "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HARASSMENT",          "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH",         "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",   "threshold": "BLOCK_NONE"},
                ]
            )

            text    = response.text
            cleaned = clean_json(text)

            try:
                data = json.loads(cleaned)
            except json.JSONDecodeError as je:
                return send(self, 500, {
                    "error": f"JSON parse error: {str(je)}",
                    "raw":   cleaned[:500]
                })

            send(self, 200, {"data": data})

        except Exception as e:
            send(self, 500, {"error": str(e)})
