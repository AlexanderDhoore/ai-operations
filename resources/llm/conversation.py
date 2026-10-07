"""A terminal conversation. History lasts until this script exits."""
import os

from openai import APIError, OpenAI

messages = [{"role": "system", "content": (
    "Explain this fictional game briefly. Moon Gate opens with 3 amber shards. "
    "The shards are not consumed. Say when the supplied rules do not answer a question."
)}]

with OpenAI(
    base_url="https://api.llm.mechatronics.be/v1",
    api_key=os.environ["VIVES_LLM_API_KEY"],
    timeout=60.0,
    max_retries=0,
) as client:
    print("Ask about the game. Type /quit to stop.")
    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if question == "/quit":
            break
        if not question:
            continue

        pending = messages + [{"role": "user", "content": question}]
        try:
            response = client.chat.completions.create(
                model="qwen3.8-27b",
                messages=pending,
                reasoning_effort="low",
                max_tokens=2048,
            )
        except APIError:
            print("The model request failed. Check the connection and settings, then try again.")
            continue

        choice = response.choices[0]
        if choice.finish_reason != "stop" or not choice.message.content:
            print("The answer was incomplete. Check the output limit or try again.")
            continue
        answer = choice.message.content
        print("Assistant:", answer)
        messages = pending + [{"role": "assistant", "content": answer}]
