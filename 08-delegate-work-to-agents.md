# 08 — Delegate work to coding agents

Your game needs two improvements. Instead of asking one agent to do everything
in sequence, you will let a **controller** divide the work between two
**workers**. Both workers change code. The controller reviews their results,
combines the changes and checks that the game still works.

You will build a small delegation system with your agent, using Pi, Screen
and Git. It extends [Assignment 07](07-work-with-pi-and-screen.md): the
controller starts the workers, and they can finish their assigned tasks even
when you close your laptop. You return later to review and integrate the work.

## What is a subagent?

A subagent is an agent that receives a task from another agent. It can read
files, use tools and return a result. Its work happens in a separate context,
so every file read and intermediate tool result need not fill the controller's
conversation. The controller still needs enough information to judge the result.

Coding harnesses such as [Codex](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[VS Code](https://code.visualstudio.com/docs/agents/run/subagents) and
[Claude Code](https://code.claude.com/docs/en/sub-agents) offer subagent workflows.
Their details differ, including which context is passed along, available tools
and whether tasks run in parallel. Delegation is a harness feature, not a
special ability that only one model has.

![The controller sends bounded tasks to two workers with separate contexts and receives reports and code changes for review](assets/08-delegation-context.svg)

Follow the arrows: the task travels out, and a result comes back. As in
[Assignment 05](05-give-your-agent-a-memory.md), useful context must be recorded
or explicitly provided. Our workers receive task files and project instructions,
not the controller's entire chat. Their requests still consume tokens. Separate
contexts reduce what accumulates in the controller's conversation, not all usage.

Three ideas matter here:

| Idea | What it means |
| --- | --- |
| Delegation | Another agent gets a bounded task and reports its result. |
| Parallel work | More than one task can make progress at the same time. |
| Independent lifetime | A worker can keep running after the controller disconnects. |

An asynchronous subagent is not automatically independent of its controller.
In our implementation, **Screen on the server keeps each Pi process alive**.
The controller does not need to remain open while those processes work.

## Choose your controller

The familiar baseline is **VS Code Chat with Qwen**, connected to your game
through Remote SSH. The workers also use Qwen, through Pi on the server.

You can use another coding client as controller if it can read and edit the
server's project files and run commands there. For example, eligible existing
subscriptions can provide access through [Codex](https://learn.chatgpt.com/docs/auth)
or [Claude Code](https://code.claude.com/docs/en/overview). Configure that client's
server access and project instructions before using it. Ordinary chat access
alone does not provide a server terminal.

You do not need a paid subscription for this assignment. **If you already have
one, try using a more capable GPT or Claude model as your controller.** Let it
plan the tasks, review the results and integrate the changes, while the
lower-cost Qwen workers do the implementation.

This is a useful orchestration pattern: use a stronger model where its judgment
adds value, and delegate suitable work to a cheaper model. Worker requests go
to the school endpoint instead of using your subscription allowance. Planning
and reviewing still use that allowance. Compare how well your controller
divides the work and catches problems in the workers' results.

## Give each worker its own files

Two agents editing one working directory can interfere with each other.
A **Git worktree** gives a branch its own checked-out directory while sharing
the repository's history. Each worker gets one branch and one worktree.
See the [Git worktree documentation](https://git-scm.com/docs/git-worktree).

The controller keeps the original game folder and uses an integration branch
there. No extra controller worktree is needed for this exercise.

![One primary checkout for controller integration, two separate worker worktrees on the LXC, and review before merging both branches](assets/08-worktrees-and-review.svg)

Both workers start from the same committed project state, including `AGENTS.md`,
`MEMORY.md` and `.agents/skills/`. They can read the same recorded knowledge.
The controller owns updates to central memory, while each worker reports its
own changes and checks separately.

Worktrees separate files, not permissions or shared databases and ports.
They also do not eliminate merge conflicts. Prefer independent tasks for this
first exercise. More workers will not necessarily make a shared Qwen server
faster, and reviewing their changes takes time too.

## Build the small launcher with your agent

Continue in your game on the development server. Pi and Screen should already
work from Assignment 07. Let your controller read the
[worker setup guide](resources/workers/README.md) and its linked reference files.
The reference is deliberately small enough to inspect and adapt.

Give your controller this prompt, together with the guide's URL or contents:

> Help me add the Assignment 08 delegation workflow to this game. Read the
> worker setup guide and linked files, then inspect our project and explain
> your plan before making changes.
>
> Adapt the reference launcher into scripts/worker.sh, the worker role into
> scripts/worker-role.md, and the delegation skill into
> .agents/skills/delegate-work/SKILL.md. Preserve useful existing content.
> Add /.workers/ to .gitignore. Keep our existing Pi provider configuration.
>
> Reconcile AGENTS.md and our GitHub skill with this workflow. Workers execute
> tasks we already agreed on, report separately, and do not update central
> memory, commit or push. The controller reviews, commits and integrates.
> Preserve our normal collaboration rules outside delegated tasks.
>
> Explain how to start a worker, inspect its progress and retrieve its result.
> Check the Bash syntax and installed Pi options. Do not launch workers,
> change game behavior or publish anything yet.

Review the files with the agent. Ask it to walk you through the command that
starts Pi. **`--print` means a non-interactive run**, not a read-only run:
Pi can edit and run tools, then exits after responding. The launcher supplies
the task, saves output and returns immediately. See [Pi's CLI modes](https://pi.dev/docs/latest/cli-integration).

This combines the previous lessons: instructions and memory describe the
project, a skill teaches a repeatable workflow, and a script handles the
mechanical steps. The agent helps build the system that delegates its work.

## Agree on two tasks

Choose two useful improvements with your controller. For example:

- A reset button and a separate help page explaining the rules.
- One backend endpoint and an unrelated visual improvement.
- A scoring function and an independent settings screen.

If one feature depends on an interface the other worker has not designed yet,
agree that interface first or choose a different pair. Keep the first tasks small.

Ask the controller to record the plan in memory and write two local task files
under `.workers/tasks/`. Each should give the goal, files or area to change,
expected behavior, relevant context and checks. For example:

```text
Task: add a reset button to the star game.
Change index.html only. Reset returns the counter to zero, including when
already at zero. Collecting stars still works afterwards. Preserve the
existing animation and make the button usable by keyboard.
Check the behavior you can test and report any untested parts.
The controller handles commits and central memory. Follow the worker role.
```

Have the controller review and commit the setup and agreed project state,
then create an integration branch such as `work/delegation`. Worktrees start
from a commit, so uncommitted game changes will not appear in the workers.
Task files and run logs stay local and ignored.

## Delegate, then leave the workers to work

Ask your controller:

> Use our delegation skill to start the two agreed tasks from the same commit.
> Give each worker a different ID and its own worktree. Report the IDs,
> branches and result locations, then return to me without waiting for completion.
> Do not push or merge anything yet.

Underneath, the controller runs commands like these in the game folder:

```bash
bash scripts/worker.sh start reset .workers/tasks/reset.md
bash scripts/worker.sh start help .workers/tasks/help.md
```

Use your actual IDs and task filenames. The launcher creates the worktrees in
a sibling folder such as `YOUR-GAME-workers/` and starts a named Screen session
for each worker. There is no need to open Pi interactively yourself.

You can close the controller and terminal as in Assignment 07. The workers
continue their assigned tasks on the server, then exit. They do not invent
new tasks while you are away. Their task files, output and changes remain.

## Return, review and integrate

Reconnect to the game folder and ask the controller to inspect the existing
jobs. A fresh chat can use the saved records instead of starting duplicates:

```bash
bash scripts/worker.sh status reset
bash scripts/worker.sh result reset
```

Repeat for the other ID. A finished Screen session may disappear because Pi
exited normally. The records under `.workers/ID/` remain. An empty output log
while Pi is working does not by itself indicate failure.

**A finished process is not an approved change.** Read the report and inspect
the actual diff and any new files. A worker may have stopped with a question,
missed a requirement or reported checks it could not run.

Ask your controller:

> Review both tasks and their actual worktree changes, including new files.
> Run suitable checks and resolve problems before accepting the work. Only
> edit a worker's files after it has stopped. Explain any remaining limitations.
>
> Commit the reviewed changes on their worker branches and merge the accepted
> branches one at a time into our integration branch. You are authorized to
> make these local commits and merges. Check the combined game as well.
> Update project memory with the outcome and next step. Do not push or merge
> main yet.

Try the combined game yourself. For the reset/help example, check that the
button works and that the help page is reachable and describes the actual
behavior. A successful Git merge alone does not establish either.

When satisfied, ask the controller to finish publishing through your agreed
GitHub workflow. Keep the worker records until review is complete. Afterwards,
let it remove clean, merged worktrees and their branches, preserving any
unfinished work.

## What could come next?

We deliberately built a small, visible workflow. It has no automatic retries,
crash recovery or continuously running coordinator. For larger systems, explore
Pi's [official subagent example](https://github.com/earendil-works/pi/tree/main/packages/coding-agent/examples/extensions/subagent),
extensions such as [pi-subagents](https://github.com/fitchmultz/pi-subagents), or
the experimental [Pi Durable library](https://github.com/earendil-works/pi/tree/main/packages/durable).
Compare how they handle task lifetime, results and isolation before adopting one.
You do not need to install them for this assignment.

## Be ready to discuss

Explain how you divided the work, where the controller and workers ran, what
continued after disconnecting, and how you decided the changes were ready to
combine. Discuss anything the controller caught during review and what you
would change about your next pair of tasks.
