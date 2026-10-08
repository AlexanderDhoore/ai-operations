"""A fresh one-tool experiment. No game files or previous chat script needed."""
import json
import os
import sys

from openai import APIError, OpenAI

# Fictional server data. In a game, obtain this identity from the trusted session.
SESSION_PLAYER = "alice"
PLAYERS = {
    "alice": {"location": "Moon Gate", "inventory": {"amber_shards": 2}},
    "bob": {"location": "Hidden Vault", "inventory": {"secret_card": "owl"}},
}
MAX_MODEL_REQUESTS = 4
MAX_TOOL_CALLS = 6


def get_player_state(player_id):
    """Return only this player's location and inventory."""
    if player_id not in PLAYERS:
        raise ValueError("No authenticated player.")
    state = PLAYERS[player_id]
    return {"location": state["location"], "inventory": dict(state["inventory"])}


TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_player_state",
        "description": "Read the current player's location and inventory.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    },
}]


def dispatch(name, raw_arguments, player_id):
    """The model supplies a name and JSON, never Python code to execute."""
    if name != "get_player_state":
        raise ValueError("Unknown tool.")
    arguments = json.loads(raw_arguments)
    if arguments != {}:
        raise ValueError("This tool takes no arguments.")
    return get_player_state(player_id)


def answer_question(client, question, player_id):
    messages = [
        {"role": "system", "content": (
            "Help a player understand their current game situation. "
            "Use the available tools for current facts. Do not invent missing "
            "facts or rules. If a tool reports an error, explain the limitation. "
            "Answer briefly."
        )},
        {"role": "user", "content": question},
    ]
    calls_used = 0
    for request_number in range(1, MAX_MODEL_REQUESTS + 1):
        print(f"Model request {request_number}")
        response = client.chat.completions.create(
            model="qwen3.8-27b", messages=messages, tools=TOOLS,
            reasoning_effort="low", max_tokens=2048,
        )
        choice = response.choices[0]
        message = choice.message
        if choice.finish_reason not in ("stop", "tool_calls"):
            raise RuntimeError("The model response was incomplete. No tools were executed from it.")
        if not message.tool_calls:
            if choice.finish_reason != "stop" or not message.content:
                raise RuntimeError("The model returned no complete answer.")
            return message.content
        if request_number == MAX_MODEL_REQUESTS or calls_used + len(message.tool_calls) > MAX_TOOL_CALLS:
            raise RuntimeError("The tool budget was reached. Try a smaller question.")

        # Keep every requested call so each tool result has a matching ID.
        messages.append({
            "role": "assistant", "content": message.content,
            "tool_calls": [{
                "id": call.id, "type": "function",
                "function": {"name": call.function.name, "arguments": call.function.arguments},
            } for call in message.tool_calls],
        })
        for call in message.tool_calls:
            calls_used += 1
            try:
                result = dispatch(call.function.name, call.function.arguments, player_id)
            except ValueError as error:
                result = {"error": str(error)}
            print("Tool:", call.function.name, "Arguments:", call.function.arguments)
            print("Result:", json.dumps(result))
            messages.append({
                "role": "tool", "tool_call_id": call.id, "content": json.dumps(result),
            })
    raise RuntimeError("No answer within the request budget.")


def main():
    question = " ".join(sys.argv[1:]) or "Where am I and how many amber shards am I carrying?"
    print("Question:", question)
    with OpenAI(
        base_url="https://api.llm.mechatronics.be/v1",
        api_key=os.environ["VIVES_LLM_API_KEY"],
        timeout=60.0, max_retries=0,
    ) as client:
        try:
            print("Assistant:", answer_question(client, question, SESSION_PLAYER))
        except APIError:
            raise SystemExit("The model request failed. Check the connection and settings.")
        except RuntimeError as error:
            raise SystemExit(str(error))


if __name__ == "__main__":
    main()
