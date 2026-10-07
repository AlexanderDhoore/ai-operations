# A small Pi worker launcher

This is the reference implementation for [Assignment 08](../../08-delegate-work-to-agents.md).
It uses Bash, Git, Screen and the Pi/Qwen configuration from Assignment 07.
No extension, orchestration service or additional credential is needed.
The [rehearsal record](VALIDATION.md) describes the tested setup and its limits.

## Install with your controller

Have your agent read and adapt these files to your game:

| Course resource | Destination in the game |
| --- | --- |
| [worker.sh](worker.sh) | `scripts/worker.sh` |
| [worker-role.md](worker-role.md) | `scripts/worker-role.md` |
| [SKILL.md](SKILL.md) | `.agents/skills/delegate-work/SKILL.md` |

Add `/.workers/` to the game's `.gitignore`, preserving existing entries.
Keep the script, role and skill tracked. Review the project resources before
running them. Pi's `--approve` trusts those resources for the worker invocation.
It does not sandbox tools. Worktrees separate files, not Linux permissions.

Reconcile existing agreements too. For example, the previous GitHub skill
may assume a single branch, and AGENTS.md may tell every agent to update
MEMORY.md or wait for agreement. Add a short exception for **agreed delegated
tasks**: workers follow `scripts/worker-role.md`, report instead of editing
central memory, and leave commits and integration to the controller. Preserve
the normal collaboration rules for other work. No second memory system is needed.

Finish setup on an integration branch: check the script and installed Pi options,
review the changes, update memory and make the local setup commit authorized by
the assignment prompt. Verify a clean checkout and ignored runtime files before
reporting that setup is ready. Preserve unrelated changes and report any blocker.
After agreeing on worker tasks, commit any new plan updates before launching too.

The supplied script intentionally has only three commands:

```bash
bash scripts/worker.sh start reset .workers/tasks/reset.md
bash scripts/worker.sh status reset
bash scripts/worker.sh result reset
```

The controller runs these on the development server, in the primary game checkout,
through its terminal tool or SSH. Students ask it to delegate work and check
progress rather than running the commands themselves. `start` returns after
launching, not after Pi finishes. Use different IDs for different runs.

## What the script does

`start` requires a clean committed checkout. This ensures workers get the code,
instructions and skills you reviewed, since a worktree starts from a commit.
It creates `worker/ID` and a worktree at `../YOUR-GAME-workers/ID`, saves the
task and role, then starts Pi in a detached Screen session. Both workers should
start from the same commit before the controller begins integration.

The essential command, run **inside the worker's directory**, is:

```bash
pi --provider vives --model qwen3.8-27b --thinking medium \
  --approve --print --session-dir "$job/sessions" \
  --append-system-prompt "$job/role.md" "@$job/task.md"
```

Here, `$job` is that job's absolute record directory, set by the launcher.
`--print` runs one assignment without an interactive UI and exits afterwards.
The agent can still read, edit and run tools. `@file` supplies the task text.
The appended role assigns worker responsibilities, while the worktree supplies
the project's existing context and skills. See the [Pi CLI reference](https://pi.dev/docs/latest/cli).

The launcher writes these local records:

```text
.workers/reset/
├── task.md, role.md       # instructions used for this run
├── base, worktree, screen # commit, location and session identity
├── status, exit-code     # last recorded process outcome
├── output.log            # Pi's text output and errors
├── sessions/             # Pi session records with tool activity
└── run.sh                # the small script executed inside Screen
```

`result` can be empty while Pi is thinking. Inspect session records for detailed
activity if necessary. **Finished means review is required**, even with exit
code zero. The report can describe a blocker or incomplete checks.

Workers do not commit. The controller inspects `git -C WORKTREE status`, diffs
and untracked files, then stages specific accepted paths and commits them on
the worker branch. Only then does it merge that branch into the integration
branch and check the combined game. No push or merge to main is automatic.

## Deliberate limits

This is a teaching script, not a job scheduler. It has no automatic retries,
crash recovery or notification system. Status is a saved observation, not a
live health check. If a run disappears before recording an exit, inspect its
named Screen session and logs before deciding what to do.

For this exercise, workers should run finite checks, not leave development
servers running. Worktrees do not isolate ports, databases or other services.
If your checks need those, agree separate resources first.

Keep worktrees and records until review is complete. Afterwards, have the
controller remove clean, merged worktrees with `git worktree remove`, then
delete their merged branches with `git branch -d`. Do not force-remove work
that still contains changes. Local logs may contain project details and do
not belong in Git.
