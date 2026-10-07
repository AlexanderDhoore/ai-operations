"""Optional: an answer and suggested questions for a future chat interface."""
import json
import os

from openai import OpenAI

schema = {
    "type": "object",
    "properties": {
        "answer": {"type": "string"},
        "suggested_questions": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["answer", "suggested_questions"],
    "additionalProperties": False,
}

with OpenAI(
    base_url="https://api.llm.mechatronics.be/v1",
    api_key=os.environ["VIVES_LLM_API_KEY"],
    timeout=60.0,
    max_retries=0,
) as client:
    response = client.chat.completions.create(
        model="qwen3.8-27b",
        messages=[
            {"role": "system", "content": (
                "Explain this fictional game using only these rules: "
                "Moon Gate opens with 3 amber shards. The shards are not consumed. "
                "Return JSON with answer as a short plain-language answer, "
                "and suggested_questions as two brief questions the player could ask next. "
                "Do not put JSON inside the answer string."
            )},
            {"role": "user", "content": "How do I open Moon Gate?"},
        ],
        reasoning_effort="low",
        max_tokens=2048,
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "game_answer", "strict": True, "schema": schema},
        },
    )
    choice = response.choices[0]
    if choice.finish_reason != "stop" or not choice.message.content:
        raise RuntimeError("No complete structured answer.")
    result = json.loads(choice.message.content)
    if not isinstance(result, dict) or set(result) != {"answer", "suggested_questions"}:
        raise ValueError("Unexpected answer structure.")
    if not isinstance(result["answer"], str):
        raise ValueError("The answer must be text.")
    questions = result["suggested_questions"]
    if not isinstance(questions, list) or any(not isinstance(q, str) for q in questions):
        raise ValueError("Suggested questions must be a list of strings.")
    print(json.dumps(result, indent=2))
