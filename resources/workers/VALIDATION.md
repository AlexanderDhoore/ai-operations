# Assignment 08 rehearsal

The reference launcher was rehearsed with two real Pi/Qwen workers on the
instructor's development container. This records evidence and limits for
review, not extra student requirements.

## Environment and isolation

- Pi 1.0.4, Node 22.23.3 and GNU Screen on `ai-operations-01`.
- Existing `vives` provider with `qwen3.8-27b`, medium thinking.
- An isolated local clone of the small star game, with its remote removed.
  The original game checkout and its existing memory change were preserved.
- The controller used SSH commands. VS Code's UI and alternative controller
  subscription clients were not exercised in this rehearsal.

## Observed workflow

1. Prepared committed instructions, memory, launcher and delegation skill.
2. Started both workers from the same commit in separate worktrees.
   One added a reset button to `index.html`, the other created `help.html`.
3. The launching SSH connection ended immediately. A separate connection
   observed both named Screen sessions detached and both jobs running.
4. Both Pi processes completed with exit code zero and saved reports. Session
   records showed both reading their own AGENTS.md and MEMORY.md. The reset
   worker also read the delegation skill. Neither worker changed central
   memory or committed its code.
5. The controller reviewed the diff and new file, committed on each worker
   branch, merged both and added the link connecting the game to its help page.
6. A real local Chromium browser tested exact copies of the integrated HTML:
   collecting twice, keyboard reset, reset at zero, collecting after reset,
   help navigation and return. All passed with no JavaScript page errors.
7. The integrated rehearsal checkout was committed and left clean. Both Pi
   processes and their Screen sessions ended. Records and worktrees remain
   available for instructor inspection.

The browser check validates these static pages, not a deployed game backend.
Neither worker had run a browser itself, and both disclosed that limitation.

## Launcher checks

A temporary Git fixture used real Screen and a stub Pi executable to verify
detached execution, successful and nonzero exits, output capture, paths with
spaces, duplicate and invalid ID rejection, and refusal to start from a dirty
checkout. The fixture was removed afterwards. Bash syntax checks passed.

These checks do not establish crash recovery or production reliability.
The launcher intentionally does not provide either.
