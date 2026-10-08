# Assignment 10 verification

Rehearsed on the instructor's `ai-operations-01` development container on
2026-10-08, using Python 3.13.5, OpenAI SDK 3.26.0 and the school's
`qwen3.8-27b` Chat Completions endpoint.

## Live observations

The published `one_tool.py` ran unchanged in an isolated directory. A private
second-tool prototype checked the feasibility of the student extension. That
extension is not supplied as a course solution.

| Scenario | Observed result |
| --- | --- |
| Default starter question | Called `get_player_state`, then answered Moon Gate and two amber shards. |
| Changed inventory | Read five shards and answered with the changed value. |
| Opponent's secret card | The returned state contained only the selected player's fields. The answer did not reveal the other player's card. |
| General meaning of inventory | Answered without requesting a tool. |
| Private two-tool extension | Read inventory and gate requirements, then identified one missing shard. |
| Changed gate requirement | With seven required and two held, identified five missing shards. |
| Unavailable gate | Returned a tool error and explained that the requested information was unavailable. |

These are observations of particular requests, not guarantees of model behavior.
The access boundary is the backend's selection of data. A model's refusal alone
does not establish that boundary. The unavailable-gate answer also suggested
possible reasons for the failure, so factual wording still needs review.

## Deterministic checks

Eight local simulated-response checks covered ordinary answers, multiple calls
with matching result IDs, rejection of invalid calls and unknown sessions, error
results, truncated calls, request and call budgets, and empty final answers.
They also checked that the model's messages did not contain the other player's
secret data. The starter uses a fixed demonstration identity, not real login.

## Scope and preservation

The rehearsal used synthetic data and the existing private credential. Its writes
were confined to the temporary rehearsal directory. That directory and virtual
environment were removed after collecting sanitized results. The original game
was not reset or edited by the rehearsal.

The game's HEAD and status listing, plus the checked private configuration,
matched the baseline. Its existing working diff changed during the rehearsal,
so a claim that all game contents remained identical cannot be made.

The container lacked `ensurepip`. As in the earlier SDK rehearsal, pip was
bootstrapped inside the isolated environment without installing system packages.
The Debian package-install alternative was not exercised. No student's game
integration, authentication system, browser UI or classroom load was tested.
