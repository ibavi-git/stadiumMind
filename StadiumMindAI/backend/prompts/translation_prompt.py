import json

def build_translation_prompt(text: str, target_language: str, context_type: str, context: dict) -> str:
    stadium = context.get('stadium', {})
    match = context.get('match', {})
    
    prompt = f"""You are the FIFA multilingual stadium communications specialist.
Domain Context:
- Stadium: {stadium.get('name')}
- Match: {match.get('match_name')}

Context Type Rules:
- emergency = urgent imperative
- announcement = formal broadcast
- instruction = direct
- general = natural

Current Context Type: {context_type}

Translate the following text to {target_language}.
Keep proper nouns, gate names, zone labels in original form.
Provide context notes explaining any translation decisions.

Text to translate:
{text}

Return JSON with no markdown fences, no formatting:
{{
  "translated": "...",
  "context_notes": "..."
}}
ONLY return the JSON object.
"""
    return prompt
