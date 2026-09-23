# 01 — Start building with VS Code Chat

<img src="assets/vscode-stable.png" alt="Visual Studio Code icon" width="72">

Your first task is to set up **VS Code Copilot Chat** on your own computer,
connect it to the Mechatronics LLM cluster's Qwen model, and begin your game.
Follow the [Mechatronics LLM guide](https://docs.mechatronics.be/llm/) to create
your personal API key and complete the VS Code Copilot Chat setup. The guide
is behind the Mechatronics login; ask in class if you cannot access it.

Keep your API key private. It belongs in your tool's private configuration,
never in project files, screenshots, or a Git repository. Your assistant can
read and run things with the permissions of your own computer account, so
check what it proposes before you run or accept it.

## Build the first slice

Choose a multiplayer game idea that you can explain in a few sentences.
Research a possible frontend and backend, then choose the smallest version
that you can run in a browser. Work with your assistant to create that first
playable slice. A screen that responds to a player's action is a good start;
two connected players sharing state is the direction you will build toward,
not a requirement to finish in this first class.

Start by asking the assistant to discuss your idea and the likely architecture
before it writes code. Then give it one small task at a time. Run what it
builds, inspect the changes, and ask it to explain anything you cannot yet
explain yourself. If you encounter setup or dependency problems on your own
computer, work through them and note what happened; we will revisit the
development environment later in the course.

## Be ready to show

By the end of this first stage, you should be able to show:

- VS Code Chat making a request to the Mechatronics model.
- Your game idea, a running browser prototype, and how to start it again.
- A brief explanation of your technology choices.

The prototype can be rough. Make one small part work and understand it.
GitHub, pull requests, remote development, and deployment will be introduced
in later assignments.
