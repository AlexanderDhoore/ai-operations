# 05 — Give your agent a memory

Your coding agent has helped you build a game, work on a Linux server, and
use GitHub. But a long conversation is a fragile place to keep your project's
plan. In this assignment, you will give the agent a small memory system:
two Markdown files in your game repository, kept useful as the work changes.
You will finish by opening a new chat and checking whether it can pick up
where you left off.

## What fits in context?

A language model processes **tokens**, not a simple count of words or letters.
A tokenizer turns text into a sequence of units represented by numbers. A unit
might correspond to a whole word, part of a word, punctuation, or whitespace.
Code is tokenized too: variable names, operators and indentation all contribute.

GPT, Claude and Qwen models can use different tokenizers, so the same sentence
or program can have different token counts. You do not need to calculate
these by hand. Just remember that token count is different from word count.

The **context window** is the bounded amount of information a model can work
with in one request. Your latest message is only part of it. Instructions,
available tool definitions, earlier exchanges, selected file contents and tool
results also take space. Customizations can contribute instructions too. We
will discuss skills in a later assignment.

The agent assembles context for each model request. Long command outputs and
file reads add tokens too. Opening a repository does not automatically put
all its contents into context.

![A request becomes tokens, and growing history is compacted to make room](assets/05-context-compaction.svg)

Open the context indicator in your VS Code Chat session and inspect the
**Session Info** popup. In our walkthrough it showed **21.9K / 131K tokens**,
with space used by system instructions, tool definitions and messages, plus
space reserved for the response:

![VS Code Session Info showing 21.9K of 131K tokens and the context breakdown](assets/05-context-window.png)

Notice the space used by tool definitions. Our course configuration divides
the budget into **96K tokens for input and 32K reserved for output**:

```text
 98,304 input tokens  (96 × 1,024)
+32,768 output tokens (32 × 1,024)
────────────────────────────────
131,072 tokens total (128 × 1,024)
```

VS Code rounds the total to **131K**. Instructions, tools, history and retrieved
content share the 96K input allowance. The 32K output reservation is a maximum,
not a required response length. These are our course settings from the
[Mechatronics LLM guide](https://docs.mechatronics.be/llm/), not universal Qwen
limits. The agent may compact before the input budget is full.

## What happens when the conversation grows?

As context fills, VS Code can **compact** older conversation history by
summarizing it. You can think of this as replacing detailed meeting notes with
a shorter handoff. There is room to continue, but some of the original detail
may no longer be present in the next request. The visible chat history and
what the model receives are not necessarily identical.

A summary can preserve the main goal while losing why you rejected a library,
which edge case still fails, or whether a proposed feature was ever approved.
Repeated summaries can compound that loss. A larger window gives you more
room, but it is not a guarantee that every earlier detail will be used correctly.

The agent software manages compaction, not the model server itself. VS Code
provides **Compact Conversation** and `/compact`, but you do not need to force
compaction for this assignment. See
[VS Code's context explanation](https://code.visualstudio.com/docs/agents/concepts/context#context-window-and-compaction).

## Keep useful information outside the chat

For this assignment, **memory** means ordinary files that survive the chat.
Writing a decision down gives the next conversation something concrete to
read. It does not train the model or make the file magically available. The
agent must retrieve it, and the retrieved text still takes space in context.

Some memory systems use databases such as SQLite or store relationships in
knowledge graphs. Our system will stay small enough to read, review and track
with Git. Use this same layout at the root of your game repository:

```text
YOUR-GAME/
├── AGENTS.md
├── MEMORY.md
└── ...your existing game files
```

`MEMORY.md` is the **changing working record**. It holds the goal, agreed plan,
important decisions, progress and checks, and the next step. Update it when
work changes. Replace stale statements rather than appending every exchange.
Record what actually happened, including what remains untested.

`AGENTS.md` holds the **stable collaboration instructions**. It tells the agent
where memory lives, when to read it, and how to maintain it. Stable does not
mean immutable, but finishing a task should normally change `MEMORY.md`, not
the collaboration rules. Keeping the two separate makes both easier to review.

Keep secrets out of both files, even in a private repository. Write useful
project facts and decisions, not passwords, API keys or a transcript of chat.

## Create the two files in your game repository

Connect VS Code to your assigned server as in Assignment 03. Open your game's
repository folder itself, rather than its parent `/root`. The screenshot uses
the teacher's game folder. Use your own:

![Opening the game repository as the remote VS Code workspace](assets/05-open-project-folder.png)

Select your Mechatronics Qwen model in **Agent** mode. Ask:

> I want to introduce a simple memory system for this project. Inspect the
> project, then create two Markdown files at the repository root: AGENTS.md
> and MEMORY.md. If either exists, preserve its useful content.
>
> AGENTS.md should instruct you to read MEMORY.md when starting work, discuss
> and agree on a plan before implementing it, consult the plan during work,
> and update memory after meaningful progress or changed decisions. Keep
> these collaboration instructions separate from changing task status.
>
> MEMORY.md should contain: Goal, Agreed plan, Decisions, Progress and checks,
> and Next step. Use only facts you can establish from the project or our
> conversation. Mark anything unknown rather than inventing it.
>
> Keep both files concise. Do not change game code, commit, or push.

<details>
<summary>Our setup prompt in VS Code</summary>

![Asking Qwen to create the two memory files without changing game code](assets/05-create-memory-prompt.png)

</details>

Open both files and check that their contents match your project. Correct
assumptions or invented plans before continuing.

![AGENTS.md and MEMORY.md beside the existing game files in Explorer](assets/05-memory-files.png)

A minimal `AGENTS.md` can look like this. Preserve useful existing instructions:

```markdown
# Working on this game

- At the start of work, read MEMORY.md in this repository.
- Discuss the goal and agree on a plan with me before implementing it.
- Save the agreed plan in MEMORY.md and consult it during the work.
- After meaningful progress or changed decisions, update MEMORY.md.
- Record checks actually performed, their results, and what remains untested.
- Keep memory concise and current. Replace outdated information.
- Keep task progress in MEMORY.md, separate from these collaboration rules.
- Never put passwords, API keys or access tokens in either file.
- Ask before committing or pushing changes.
```

Use the same five headings in `MEMORY.md`. Here is an example from a fictional
game after some work on a restart button:

```markdown
# Project memory

## Goal
Let players restart a round without refreshing the page.

## Agreed plan
1. Add a restart button and reset the score.
2. Check the behavior with two connected players.

## Decisions
Preserve player names when restarting so players do not have to rejoin.

## Progress and checks
Restart button added. Score resets in a single-browser check.
Two-player behavior has not been checked yet.

## Next step
Open two browser windows and check that both see the restarted round.
```

Fill yours with your own project's facts. If no plan is agreed yet, say so.

## Use memory while doing real work

Choose one small improvement to your game, such as explaining its controls
more clearly or adding a restart action. Keep it small enough to try yourself.
Begin with discussion:

> I want to improve [describe one small part of the game]. Inspect what is
> relevant and propose a short plan. Discuss the choices with me before
> changing code.

Once you agree, ask the agent to write the goal, plan and decisions into
`MEMORY.md`. Read the saved plan yourself. Then ask:

> Carry out the first agreed step. Refer to MEMORY.md as you work. Run the
> relevant checks, then update memory with what changed, what was checked,
> and what remains to do. Do not commit or push yet.

Inspect the changes and try the game. Record any problems in memory, then
continue through the plan in manageable steps. Before ending the chat, ask
the agent to update `MEMORY.md` with the actual status and next step, or note
that the work is complete. Keep it current throughout the work.

## How does a new chat find the memory?

VS Code automatically includes root-level **`AGENTS.md`** as project
instructions when support is enabled. Use that exact uppercase, plural
filename on Linux. `MEMORY.md` is our own convention: the instructions tell
the agent to read and maintain it. See
[VS Code's instructions documentation](https://code.visualstudio.com/docs/agent-customization/custom-instructions#use-an-agentsmd-file).

![A fresh chat loads instructions, retrieves memory, and maintains it during work](assets/05-memory-cycle.svg)

VS Code supplies the instructions, and the agent uses them to retrieve the
working record. These instructions guide behavior. They do not grant system
permissions or enforce rules as a security boundary.

## Start a fresh chat

Save both files. Use the **+** button at the top of the Chat view to open
**New Chat** in the same VS Code workspace. Keep **Agent** mode and the same
Qwen model selected. Do not paste the old conversation, restate the plan,
or manually attach `AGENTS.md` or `MEMORY.md`. Ask:

> What is our current goal, what progress has been made, and what should we
> do next? Do not change anything yet.

Notice whether the agent uses the project instructions and reads `MEMORY.md`
without being reminded. If the response has a **References** section, you
can expand it to inspect the included instructions.

In our fresh-chat walkthrough, the agent referred to the instruction in
`AGENTS.md` to read memory first:

<details>
<summary>Our agent identifies the project instruction in the new chat</summary>

![The fresh-chat agent refers to AGENTS.md and its instruction to read MEMORY.md first](assets/05-new-chat-instructions.png)

</details>

The visible tool activity then shows it reading `MEMORY.md`, followed by the
project README and game source:

![The new chat reads MEMORY.md and inspects the project without receiving the old conversation](assets/05-new-chat-reads-memory.png)

Compare its answer with your memory file. The new chat can find your working
record because `AGENTS.md` explains where to look, even though the old
conversation is absent. A new chat is different from compaction, but both
benefit from this external record.

If the agent misses it, check that both files are saved at the workspace root
and that `AGENTS.md` directs it to read `MEMORY.md`. In VS Code Settings,
search for `chat.useAgentsMdFile` and check that it is enabled, then try again.

## Be ready to discuss

Be comfortable explaining how your agent uses the two files, what happens
when you open a new chat, and why a long conversation can lose details.
Use your own game as the example when we talk about what you tried and
how it worked. There is no separate report or screenshot collection to submit.

Review, commit and push your changes using the workflow from Assignment 04,
including the memory files so their updates are tracked with the project.
