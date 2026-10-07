---
name: delegate-work
description: Split agreed game improvements into two independent Pi worker tasks, start them on the development server, and review and integrate their results. Use when the user asks to delegate work or check existing workers.
---

# Delegate game work

Use the server's existing Pi/Qwen setup and scripts/worker.sh. Run commands in
the game's primary checkout. Inspect existing .workers records before launching
anything, so a fresh chat does not duplicate work.

1. Discuss two bounded tasks and acceptance checks with the user. Prefer
   separate files or modules. Record the agreed plan in MEMORY.md and clarify
   any shared interfaces. Preserve unrelated changes. Workers must not edit
   central memory, instructions, skills or launcher code.
2. Review and commit the setup and agreed project state before starting.
   Create an integration branch in the primary checkout. In .workers/tasks/,
   write one task file per worker with the goal, scope, acceptance checks and
   relevant project context. Task files represent work the user agreed to.
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

Commit/merge authorization comes from the user's task. If already given for
this exercise, proceed within that scope without repeated approval questions.
