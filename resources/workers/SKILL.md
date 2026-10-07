---
name: delegate-work
description: Split agreed game improvements into two independent Pi worker tasks, start them on the development server, and review and integrate their results. Use when the user asks to delegate work or check existing workers.
---

# Delegate game work

Use the server's existing Pi/Qwen setup and scripts/worker.sh. Run commands in
the game's primary checkout. Inspect existing .workers records before launching
anything, so a fresh chat does not duplicate work.
The user talks to you to delegate work and inspect progress. Run the launcher
commands yourself through your terminal tool or SSH, then explain the result.
Use the project's recorded delegation agreement for local commit and merge
authorization. A clear request to delegate can start the workflow without a
special prompt or repeated approval. Ask only about missing requirements or
unresolved scope. A progress question only inspects existing jobs. Review and
integration start when requested, not automatically after a status check.

1. Turn the user's requested improvements into two bounded tasks and acceptance
   checks. Help the user discuss expected behavior, important edge cases and
   dependencies before delegating. Use what was already agreed without making
   them repeat it. Clarify missing requirements, or proceed if the scope is clear. Prefer
   separate files or modules. Record the agreed plan in MEMORY.md and clarify
   any shared interfaces. Preserve unrelated changes. Workers must not edit
   central memory, instructions, skills or launcher code.
2. Verify setup is committed and use the integration branch in the primary
   checkout, creating it if needed. Review and commit any agreed plan updates
   within the user's authorization, then verify a clean checkout. Preserve
   unrelated work and report blockers rather than committing or discarding it.
   In .workers/tasks/, write one task file per worker with the goal, scope,
   acceptance checks and relevant project context. Task files represent work
   the user agreed to.
3. Choose unique job IDs. Use `bash scripts/worker.sh start ID TASK.md` twice
   from the same committed base, without changing HEAD between starts. The
   script creates each worker branch/worktree and starts Pi inside Screen.
   Report IDs and paths, then return to the user. Do not wait in a polling loop.
4. When asked for progress, use `status ID` and `result ID`. The output log
   contains Pi's text output, while sessions/ contains its detailed session
   records. A finished process is not proof of completed or correct work.
5. Inspect each task, report and actual worktree changes, including untracked
   files. Run suitable checks. Fix problems in the worker's worktree only once
   that worker has stopped. If the fix is substantial, agree a follow-up task
   with a new ID instead. Never merge an unfinished or blocked task as complete.
6. Stage only reviewed files and commit each accepted change on its worker
   branch, using `git -C WORKTREE ...`. Merge the accepted branches one at a
   time into the integration branch. Resolve conflicts deliberately, then
   check the combined game, including behavior across both changes.
7. Update central MEMORY.md with accepted changes, checks and next steps.
   Follow the user's publishing instructions and existing GitHub workflow.
   Do not automatically push or merge main. Keep records until review is done.
   When asked to clean up, remove only stopped, clean, merged worker worktrees
   and their merged branches, preserving unfinished work.

Commit/merge authorization comes from the user's task. If already given for
this exercise, proceed within that scope without repeated approval questions.
