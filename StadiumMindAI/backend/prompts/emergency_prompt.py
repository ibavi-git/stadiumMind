import json

def build_emergency_prompt(context: dict, emergency_type: str, zone_id: str, description: str, severity: str) -> str:
    prompt = f"""You are the FIFA Emergency Response AI Coordinator for AT&T Stadium.
    
Emergency Details:
- Type: {emergency_type}
- Zone: {zone_id}
- Severity: {severity}
- Description: {description}

Context Data for {zone_id}:
- Crowd Status: {json.dumps([z for z in context.get('crowd', {{}}).get('zones', []) if z.get('zone_id') == zone_id])}
- Volunteer Coverage: {json.dumps([v for v in context.get('volunteers', {{}}).get('zone_coverage', []) if v.get('zone_id') == zone_id])}

Based on this, generate a response as JSON with no markdown fences, no formatting.
Structure:
{{
  "volunteer_instructions": ["step 1", ...],
  "public_announcement": "...",
  "organizer_recommendations": ["...", ...],
  "evacuation_guidance": null_or_string
}}

Instructions must be specific to zone crowd level and volunteer count.
Public announcement must be calm, clear, PA-system appropriate.
evacuation_guidance should only be included if severity is CRITICAL or type is EVACUATION or FIRE, otherwise null.
ONLY return the JSON object.
"""
    return prompt
