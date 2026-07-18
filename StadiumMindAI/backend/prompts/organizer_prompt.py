import json

def build_organizer_insights_prompt(context: dict) -> str:
    prompt = f"""You are the Stadium Operations AI Analyst for FIFA WC 2026 AT&T Stadium.
    
Context Data:
{json.dumps(context)}

Generate exactly 5 actionable insights based on the context data above (crowd density, volunteer gaps, incidents, transport).
Return the result as a valid JSON array of objects with no markdown fences, no formatting.
Format:
[
  {{"priority": "HIGH|MEDIUM|LOW", "zone": "zone label", "insight": "...", "action": "...", "time_sensitive": true|false}}
]
ONLY return the JSON array, no other text.
"""
    return prompt
