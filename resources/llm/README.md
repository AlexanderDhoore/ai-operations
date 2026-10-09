# Direct LLM access for the game

This public guide supplies the school-specific setup for
[Assignment 09](../../09-add-an-ai-chat-to-your-game.md). A coding agent can read
it without access to the protected Mechatronics website. It is a reference for
small SDK experiments and later integration into the student's existing game.

Use only the ordinary OpenAI SDK and the standard library for the Python experiment.
Students using another language should adapt the same request/history pattern
with an appropriate SDK, such as the [official JavaScript/TypeScript SDK](https://developers.openai.com/api/docs/libraries).
They do not need to replace their backend or add a Python service. A browser-only
game does need a small backend to hold the API key and make model requests.

## School connection

| Setting | Value |
| --- | --- |
| API base URL | `https://api.llm.mechatronics.be/v1` |
| Model | `qwen3.8-27b` |
| API used here | Chat Completions |
| Credential variable in these examples | `VIVES_LLM_API_KEY` |
| Reasoning preference | `low` for these short experiments |
| Example output budget | `2048` tokens, including thinking |

Qwen runs on the school cluster. The Python package is a client, not a local
model or a coding harness. The backend must supply context and handle history.
It does not automatically load `AGENTS.md`, `MEMORY.md` or project skills.

## Prepare the experiment with the coding agent

Inspect the existing game directory, language and Python environment first.
Preserve game files, existing dependencies and the Pi/provider configuration.
For the Python walkthrough, create an isolated environment such as `.venv-llm/`
in the game directory and keep that environment out of Git. Use another unused
name if it already belongs to something else.

Typical commands are:

```bash
python3 -m venv .venv-llm
source .venv-llm/bin/activate
python -m pip install openai==3.26.0
```

If Debian reports that `ensurepip` is unavailable, the agent can install the
matching `python3-venv` package and retry, or use a working project environment.
Install the SDK inside the environment, not with a system-wide pip command.
The reference dependency is recorded in [requirements.txt](requirements.txt).
When integrating the feature, use the game's normal dependency management.

Start with [request.py](request.py), placed as `experiments/llm/chat.py` in the
game. Explain its contents and check its syntax. The student will run it after
loading their credential privately. This is the only complete script supplied
for Assignment 09.
When the student reaches the conversation exercise, help them extend that same
script with history and explain the changes. Build later extensions together
from the concepts in the assignment and the SDK documentation.

When reading this guide through a Raw URL, resolve the file links relative to
that URL. Keep setup and program errors separate: a missing virtual environment,
a missing key and a failed model request need different fixes.

## Student: load the key privately

In your own Bash terminal on the development server, activate the environment.
If you completed Assignment 07 with the same Linux user, load the existing key:

```bash
export VIVES_LLM_API_KEY="$(cat "$HOME/.config/ai-operations/vives-llm-key")"
```

Run this yourself, outside an agent chat. It reads the private file without
printing its contents. If the file is missing, follow the
[private key-entry step from Assignment 07](../pi/README.md#3-student-enter-the-key-privately),
then run the export again. Do not paste a key into chat, a Python file or Git.
The agent should not inspect the key value or print the environment.

The variable lasts for this terminal session. A new terminal or a separately
started backend process needs its own private configuration. The key must remain
on the server when you later connect a browser interface.

From the game directory, run:

```bash
python experiments/llm/chat.py
```

A missing `VIVES_LLM_API_KEY` error means this process has not received the key.
An HTTP authentication error needs a valid personal key with model access.
The school portal still requires the student's browser login to manage keys.

## Optional extensions

First help the student integrate the required explanation chat into their game.
After that, if they choose an extension, adapt it to their existing application.
None of the extensions is required for the game chat.

- Text streaming uses `stream=True` and reads new text from `delta.content`.
  Forward it through the existing backend and read the HTTP response incrementally
  in the browser. WebSockets and a new framework are not required. The assignment
  illustrates this with `AsyncOpenAI` and FastAPI, adapt it to the game's own stack.
  Keep per-user history and save only successful complete turns. Show interrupted
  replies as incomplete, and close the upstream stream when the client disconnects.
- Structured output uses `response_format` with `type: "json_schema"` and a
  `json_schema` object containing `name`, `strict: true` and the schema. An
  `answer` and `suggested_questions` could support a reply with follow-up buttons.
  Parse and check the returned data before using it.
- Image input places a `text` item and an `image_url` item in the user message's
  `content` list. Encode a local image as a base64 data URL for the image item.

Image input is supported, not image generation. Requests may include up to
**four images** sharing **8,847,360 effective pixels**, equivalent to one
4096×2160 DCI 4K image or four 1920×1080 Full HD images. Each tiny image counts
for at least 65,536 pixels. Total decoded image files may occupy at most **40 MiB**.
Use single-frame JPEG, PNG or WebP files embedded as **base64 data URLs**.
Remote image URLs are not supported. Oversized inputs are rejected rather than
resized automatically. Check images against these limits when building the extension.

## Keep the application simple

The terminal conversation can store messages in memory until it exits. In a web
application, isolate each user's conversation on the backend. Keep trusted game
instructions separate from player messages. For longer use, bound the retained
history while preserving the instructions. No database or automatic summarizer
is required for this assignment.

The starter stops on an incomplete answer. When extending it, keep failed turns
out of conversation history and show a useful error if the model is unavailable.
An output limit also covers thinking, so a tiny limit can produce no visible text.
Check `finish_reason` before using the answer. A valid JSON object still needs
field checks, and a schema does not establish that an answer is factually correct.

The cluster supports `low`, `medium` and `xhigh` reasoning. Thinking stays enabled.
It has a 131,072-token total context and at most 32,768 output tokens. Input,
history and output share that budget. The server controls sampling settings, so
do not assume that changing `temperature` changes this endpoint's behavior.

Tools and document lookup belong to later assignments. Do not give the in-game
chat shell access or connect it to the development agent's skills and credentials.

## References

- [OpenAI Python SDK](https://developers.openai.com/api/reference/python)
- [Conversation context](https://developers.openai.com/api/docs/guides/conversation-state)
- [Structured output](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=chat)
- [Image input](https://developers.openai.com/api/docs/guides/images-vision?api-mode=chat)
- [School guide](https://docs.mechatronics.be/llm/) (browser login required)

The starter was prepared with Python 3.13 and OpenAI SDK 3.26.0. Keep its
connection details aligned with the school guide when the service changes.
See [verification notes](VALIDATION.md) for the live checks and their limits.
