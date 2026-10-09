# A one-tool experiment for Assignment 10

This public guide accompanies
[Assignment 10](../../10-give-your-game-assistant-tools.md). Start with a fresh
experiment in the student's existing game repository. Their modified script
from Assignment 09 is not a prerequisite.

## Prepare the starter

Inspect the project's language, existing environment and files first. For the
Python walkthrough, place [one_tool.py](one_tool.py) at
`experiments/llm/tools.py`, choosing another name if that path is already used.
Preserve the student's previous experiments and game implementation.

Use the [SDK setup guide](../llm/README.md#school-connection) for the school
connection details, isolated environment and private key-loading step. The
starter uses OpenAI SDK 3.26.0 and the standard library, with the same
`VIVES_LLM_API_KEY` variable. Dependencies are recorded in
[requirements.txt](../llm/requirements.txt). Use this lesson's `one_tool.py`
as the starting script. Resolve linked files relative to the guide's Raw URL.

Explain the starter, then let the student run it from their game folder in the
activated environment with their key loaded privately:

```bash
python experiments/llm/tools.py
```

It asks about a fictional player's location and inventory. An alternative
question can be passed as one quoted argument:

```bash
python experiments/llm/tools.py "Where am I?"
```

Each run begins a fresh question. The messages retained inside the function
belong to its tool-calling exchange, not a persistent interactive conversation.
The tool reads a small Python dictionary, not the student's actual game database.

## What the starter demonstrates

- `get_player_state` returns only the selected player's location and inventory.
- `TOOLS` describes the function to the model. It does not send the Python
  implementation or the contents of the player dictionary.
- `dispatch` checks the requested name and JSON arguments before calling the
  function. The model cannot supply a player ID to this tool.
- `answer_question` keeps the assistant's tool requests and returns a result
  for each `tool_call_id`. It handles multiple calls even though only one tool
  is initially available. An answer without tool calls ends the loop.

`SESSION_PLAYER` is a hard-coded demonstration identity. It is not an authentication
system. In the real game, derive identity from the trusted backend session and
apply normal visibility rules. Never accept a model-supplied identity as authority.

The starter permits at most four model requests and six tool calls per question.
Each request has a 60-second SDK timeout and retries are disabled. There is no
separate whole-question deadline. Incomplete responses stop before tool execution.
Invalid calls return an error result rather than invoking an arbitrary function.
Development traces print the fictional arguments and results. They are not a
recommendation to log private player data in a deployed application.

## Help the student extend it

After they understand the first tool, build a second read-only tool together.
For the teaching example, it accepts a gate name and returns that gate's opening
requirements from a small explicit mapping. Validate arguments and handle an
unknown gate. Update the catalog and the explicit dispatcher, then inspect a
question that needs both inventory and gate requirements. Keep results as data,
with their matching call IDs, so the model can use them in its answer.

Later, adapt the mechanism to the student's existing game chat and backend
language. Select useful state-reading capabilities for that game. Keep the API
key and access checks on the backend, and keep each player's chat separate.
No additional agent framework is needed.

State-changing tools are an optional game extension after the read-only exercise.
Discuss one action that makes the chat part of gameplay. Use existing backend game
actions and enforce player permissions, costs and current-state checks there.
Prevent duplicate execution and request player confirmation for consequential
or irreversible actions. Return the actual outcome, not an assumed success.
Keep the starter and required exercise read-only.

The model can request zero, one or several calls. Process every returned call,
even if a provider accepts a preference such as `parallel_tool_calls=False`.
Do not dispatch truncated or unparseable arguments. Old tool results in history
describe an earlier observation, query again when the question needs current state.

Use plain-text final answers for this exercise. In school-endpoint probes,
combining tools with a final `response_format` sometimes skipped tool use.
If a student's optional UI needs structured output, first collect the facts
through tools, then make a separate formatting request without tools.

See the [official function-calling documentation](https://developers.openai.com/api/docs/guides/function-calling?api-mode=chat)
for the Chat Completions message format. Keep the school's endpoint and model
when adapting those examples. [Verification notes](VALIDATION.md) record what
was rehearsed and what remains specific to each student's implementation.
