# Assignment 09 verification

Verified on the instructor's `ai-operations-01` development container on
2026-10-07, using Python 3.13.5, OpenAI SDK 3.26.0 and `qwen3.8-27b` through
`https://api.llm.mechatronics.be/v1`.

The rehearsal ran the reference files unchanged in an isolated directory.
Credentials came from the existing private key file and were not saved in
course files or results. The original game and checked private configuration
matched their baseline fingerprints afterwards. The temporary remote directory
and environment were removed.

| Check | Observed result |
| --- | --- |
| `request.py` | Answered the supplied Moon Gate rule correctly. |
| `conversation.py` | Answered a follow-up and recalled a name supplied in an earlier turn. A fresh process did not know that name. `/quit` ended the script. |
| `structured.py` | Returned the required `answer` and `suggested_questions` fields, passed the Python checks and explained the supplied rule. |
| `vision.py` | Correctly described a synthetic image with a red left half and blue right half. |
| Inline lesson code | The one-request example matched the executable reference. The conversation fragment ran successfully inside the documented client context, with the example game rules supplied. |
| Private key/environment commands | Environment activation, private key loading and script execution worked in the rehearsal terminal. |

A separate local simulated-response check confirmed that failed requests and
truncated answers do not enter conversation history. Successful user and assistant
messages do enter the next request.

The host lacked `ensurepip`, so this rehearsal created the virtual environment
without pip and bootstrapped pip privately. It did not install system packages.
The guide's alternative of installing Debian's matching `python3-venv` package
was not exercised. No game UI or particular student's backend was built in this
rehearsal. Image limits are documented from the school policy, the image test did
not exhaust every boundary. Model wording can vary between runs.
