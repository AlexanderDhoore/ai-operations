# 01 — Start building with an AI assistant

Your first task is to get an AI coding assistant working with the Mechatronics
LLM cluster and begin your game on your own computer. You can use **Pi** or
**VS Code Copilot Chat**. Both can use the cluster's Qwen model. Follow the
[Mechatronics LLM guide](https://docs.mechatronics.be/llm/) for account access,
a personal API key, and the current setup instructions for your chosen tool.
The guide is behind the Mechatronics login; ask in class if your account or
invitation is not ready.

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

- Your chosen assistant making a request to the Mechatronics model.
- Your game idea, a running browser prototype, and how to start it again.
- A brief explanation of your technology choices and what your code does so
  far, including one decision you checked or changed after an AI suggestion.

The prototype can be rough. Make one small part work and understand it.
GitHub, pull requests, remote development, and deployment will be introduced
in later assignments.
