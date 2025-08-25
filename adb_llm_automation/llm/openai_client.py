from __future__ import annotations
import os
from typing import List

# Optional OpenAI fallback planner. Only used if OPENAI_API_KEY is present.

def plan_with_llm(prompt: str) -> List[str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set; LLM planning disabled.")
    # Intentionally left as a stub to avoid hard dependencies / costs.
    # You can integrate OpenAI's Responses API here to convert `prompt` into step lines.
    # Return a list of lines like: ["tap 500x600", "type hello", ...]
    raise NotImplementedError("Hook up your preferred LLM provider here.")