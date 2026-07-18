import json
from typing import Optional

def build_volunteer_prompt(context: dict, question: str, volunteer_id: Optional[str], language: str) -> str:
    stadium = context.get('stadium', {})
    crowd = context.get('crowd', {})
    incidents = context.get('incidents', {})
    volunteers = context.get('volunteers', {})
    transport = context.get('transport', {})
    match = context.get('match', {})
    
    volunteer_context = ""
    if volunteer_id:
        roster = volunteers.get('volunteers', [])
        for v in roster:
            if v.get('id') == volunteer_id:
                volunteer_context = f"\nYou are advising volunteer {v.get('name')}, Role: {v.get('role')}, Zone: {v.get('zone')}."
                break

    prompt = f"""You are the FIFA World Cup 2026 Volunteer Co-Pilot AI.
You are assisting staff at {stadium.get('name')}.

Context Data Summaries:
- Stadium Capacity: {stadium.get('capacity')}
- Crowd Zones Status: {json.dumps(crowd.get('zones', []))}
- Active Incidents: {json.dumps(incidents.get('active_incidents', []))}
- Volunteers Summary: {json.dumps(volunteers.get('zone_coverage', []))}
- Transport: {json.dumps(transport)}
- Match Info: {json.dumps(match)}
{volunteer_context}

Please respond in {language}.
First, reason over the data.
Structure your answer exactly as:
**SITUATION:** ...
**ACTION:** ...
**REASON:** ...
**SAFETY:** (if applicable)

User Question: {question}
"""
    return prompt
