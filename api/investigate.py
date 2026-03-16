import json, os
from http.server import BaseHTTPRequestHandler
import google.generativeai as genai

KEY   = os.environ.get("GEMINI_API_KEY", "AIzaSyCd2MpD_vGXa9F-Aent9yLlqcxen3UOIJM")
MODEL = "gemini-1.5-flash-latest"

PROMPT = '''You are a forensic detective AI. Analyze the case: "{name}"

Return ONLY a raw JSON object — no markdown, no code fences, nothing else.

{{
  "case_title": "Full official case name",
  "case_summary": "2-3 sentence factual summary",
  "key_insight": "The most compelling unsolved mystery",
  "suspects": [
    {{"id":"s1","name":"Full name","role":"Primary Suspect / Witness / Victim","description":"1-2 sentences","motive":"alleged motive","status":"Never charged / Convicted / Deceased"}}
  ],
  "evidence": [
    {{"id":"e1","name":"Item name","type":"Physical / Forensic / Documentary / Testimonial","description":"significance","found_at":"where found"}}
  ],
  "locations": [
    {{"id":"l1","name":"Location name","significance":"why it matters","events":"what happened here"}}
  ],
  "timeline": [
    {{"id":"t1","date":"Date or period","event":"Title max 7 words","detail":"One sentence"}}
  ],
  "connections": [
    {{"from":"s1","to":"e1","label":"relationship","strength":"strong / moderate / weak"}}
  ],
  "insights": ["Insight 1","Insight 2","Insight 3"]
}}

Rules: 3-5 suspects, 4-7 evidence items, 2-4 locations, 5-9 timeline events, 5-10 connections.
All connection from/to values must be valid ids. Be historically accurate. Pure JSON only.'''


def cors(h):
    h.send_header("Access-Control-Allow-Origin","*")
    h.send_header("Access-Control-Allow-Methods","GET,POST,OPTIONS")
    h.send_header("Access-Control-Allow-Headers","Content-Type")

def send(h, status, data):
    body = json.dumps(data).encode()
    h.send_response(status)
    h.send_header("Content-Type","application/json")
    h.send_header("Content-Length",str(len(body)))
    cors(h)
    h.end_headers()
    h.wfile.write(body)


class handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_OPTIONS(self):
        self.send_response(204); cors(self); self.end_headers()

    def do_GET(self):
        send(self, 200, {"status":"ok","model":MODEL})

    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length",0))
            body = json.loads(self.rfile.read(n))
            name = body.get("case_name","").strip()
            if not name:
                return send(self, 400, {"error":"case_name required"})

            genai.configure(api_key=KEY)
            m = genai.GenerativeModel(MODEL)
            r = m.generate_content(
                PROMPT.format(name=name),
                generation_config=genai.GenerationConfig(
                    temperature=0.25,
                    max_output_tokens=3500,
                    response_mime_type="application/json"
                ),
                safety_settings=[
                    {"category":"HARM_CATEGORY_DANGEROUS_CONTENT","threshold":"BLOCK_NONE"},
                    {"category":"HARM_CATEGORY_HARASSMENT","threshold":"BLOCK_NONE"},
                    {"category":"HARM_CATEGORY_HATE_SPEECH","threshold":"BLOCK_NONE"},
                    {"category":"HARM_CATEGORY_SEXUALLY_EXPLICIT","threshold":"BLOCK_NONE"},
                ]
            )
            text = r.text.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
            data = json.loads(text)
            send(self, 200, {"data": data})
        except Exception as e:
            send(self, 500, {"error": str(e)})
