"""One request. Supply VIVES_LLM_API_KEY privately in the environment."""
import os

from openai import OpenAI

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
                "Explain this fictional game briefly. Moon Gate opens with "
                "3 amber shards. The shards are not consumed. "
                "Say when the supplied rules do not answer a question."
            )},
            {"role": "user", "content": "How do I open Moon Gate?"},
        ],
        reasoning_effort="low",
        max_tokens=2048,
    )
    choice = response.choices[0]
    if choice.finish_reason != "stop" or not choice.message.content:
        raise RuntimeError("No complete answer. Check the output limit or try again.")
    print(choice.message.content)
