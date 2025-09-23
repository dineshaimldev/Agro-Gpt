
import os
from typing import Tuple, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()

if _GEMINI_API_KEY:
    genai.configure(api_key=_GEMINI_API_KEY)


_SYSTEM_PROMPT = """
You are AgroGPT, an AI agricultural assistant.
Give accurate, practical, and sustainable farming guidance.
- Start with a 1–2 line summary.
- Then provide bullet points or numbered steps.
- Prefer low-cost, eco-friendly options; include safety notes.
- Call out dependencies (climate, soil, growth stage) when relevant.
- End with: "Disclaimer: Not a substitute for local expert advice."
""".strip()

_GEN_CFG = {
    "temperature": 0.4,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 1024,
}

def api_ready() -> Tuple[bool, str]:
    """
    Returns (ready, message). Frontend can show this to the user.
    """
    if not _GEMINI_API_KEY:
        return False, "GEMINI_API_KEY is missing in .env"
    try:
        
        _ = genai.GenerativeModel(_GEMINI_MODEL)
        return True, f"Gemini model ready: {_GEMINI_MODEL}"
    except Exception as e:
        return False, f"Gemini init error: {e}"

def _call_gemini(prompt: str) -> str:
    """
    Internal helper that sends a prompt with system instruction.
    Gracefully handles runtime errors and returns a friendly message.
    """
    ready, msg = api_ready()
    if not ready:
        return f"⚠ {msg}. Add your key to .env and restart.\n\nExample:\nGEMINI_API_KEY=your_key_here"

    try:
        model = genai.GenerativeModel(
            model_name=_GEMINI_MODEL,
            generation_config=_GEN_CFG,
            system_instruction=_SYSTEM_PROMPT,
        )
        resp = model.generate_content(prompt)
        text = getattr(resp, "text", "") or ""
        return text.strip() if text.strip() else "I couldn't generate a response. Please try rephrasing."
    except Exception as e:
        return f"⚠ Gemini request failed: {e}"

def get_crop_advice(crop_name: str, soil_type: str, region: str, extra: Optional[str] = "") -> str:
    """
    Returns concise, actionable advice for a crop given soil & region.
    """
    prompt = f"""
Generate practical advice for the following context:

Crop: {crop_name}
Soil type: {soil_type}
Region/Climate: {region}
Extra context (optional): {extra}

Focus areas:
- Variety/season choice (if relevant)
- Soil preparation & seed rate
- Fertilizer plan (basal, top-dress) with organic options
- Irrigation schedule by growth stage
- Common pests/diseases + IPM suggestions
- Red flags & safety notes
"""
    return _call_gemini(prompt)

def generate_report(crop_name: str, report_type: str, region: str = "", soil_type: str = "") -> str:
    """
    Builds a structured report. Supported types:
    - Fertilizer Plan
    - Pest Management
    - Yield Prediction
    """
    prompt = f"""
Create a professional report for:
- Crop: {crop_name}
- Region/Climate: {region}
- Soil type: {soil_type}
- Report Type: {report_type}

Required sections:
1) Brief Summary
2) Key Assumptions (region/soil/stage)
3) Detailed Recommendations (step-by-step)
4) Low-cost / eco-friendly alternatives
5) Safety & risk notes
6) Next actions farmers can take this week
"""
    return _call_gemini(prompt)

def ask_general(question: str, location_hint: str = "") -> str:
    """
    General Q&A entrypoint (optional).
    """
    location_txt = f"User location/context: {location_hint}\n" if location_hint else ""
    prompt = f"""{location_txt}Question: {question}
Answer clearly and practically as AgroGPT."""
    return _call_gemini(prompt)
