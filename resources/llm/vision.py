"""Optional: ask about one local PNG, JPEG or WebP image."""
import base64
import os
import sys
from pathlib import Path

from openai import OpenAI

if len(sys.argv) != 2:
    raise SystemExit("Usage: python vision.py PATH-TO-IMAGE")
path = Path(sys.argv[1])
mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(path.suffix.lower())
if mime is None:
    raise SystemExit("Choose a PNG, JPEG or WebP image.")
if path.stat().st_size > 40 * 1024 * 1024:
    raise SystemExit("The image exceeds the school's 40 MiB file limit.")
# The school endpoint also checks image dimensions and rejects animated files.
encoded = base64.b64encode(path.read_bytes()).decode("ascii")

with OpenAI(
    base_url="https://api.llm.mechatronics.be/v1",
    api_key=os.environ["VIVES_LLM_API_KEY"],
    timeout=60.0,
    max_retries=0,
) as client:
    response = client.chat.completions.create(
        model="qwen3.8-27b",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": "Describe the visible image briefly. Do not invent things you cannot see."},
            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{encoded}"}},
        ]}],
        reasoning_effort="low",
        max_tokens=2048,
    )
    choice = response.choices[0]
    if choice.finish_reason != "stop" or not choice.message.content:
        raise RuntimeError("No complete image description.")
    print(choice.message.content)
