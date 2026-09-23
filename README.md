# AI Operations

> **You have to understand what you're building.**

In this course, you will design, build, and operate a browser-based multiplayer
game. Your game is the project that connects the whole semester: you will first
use AI to help write software, then develop the practices needed to keep that
software understandable, testable, deployable, and observable. Later, you will
also explore how to integrate AI into the application itself.

You choose the game and the technologies. There is no prescribed frontend,
backend, language, or framework. Research your options, explain your choices,
and keep the scope small enough that you can make the game work end to end. By
the end of the course, people should be able to join the same game from
separate browsers and affect a shared game state.

## How the course develops

We will add requirements as the semester progresses. The broad path is:

1. **Build with an AI assistant.** Set up access to the Mechatronics LLM
   cluster and begin a small playable version on your own computer.
2. **Collaborate through GitHub.** Keep the project in a repository, make
   reviewable changes through pull requests, and use your assistant to help
   review them.
3. **Check changes automatically.** Add useful tests and GitHub Actions so
   pull requests get feedback before they are merged.
4. **Work in a consistent environment.** Move development to a provided LXC
   container and understand how it differs from your own computer.
5. **Deploy reliably.** Run the game on a separate production container, then
   automate deployment with carefully scoped credentials.
6. **Operate what you built.** Inspect logs, metrics, and dashboards; use
   monitoring to notice and diagnose problems.
7. **Integrate AI.** In the later part of the course, explore an AI capability
   within the game itself.

These are the themes, not a fixed recipe or a choice of tools on your behalf.
Each new assignment will define the requirement for that stage. You will use
official documentation, your AI assistant, experiments, and discussions with
other students to work out the implementation.

## What you are responsible for

An AI assistant can generate code and suggest commands, but you are the
engineer responsible for the result. Be able to explain the application's
architecture, the libraries you chose, how browser and server communicate,
how you test and deploy changes, and how you know the running game is healthy.
You do not need to memorize every line of code. You should be able to find the
important parts of your codebase and explain how they fit together.

At the end of the semester, you will demonstrate your live game and defend
your work in a conversation with the instructor. We should be able to inspect
the running system, examine the code and its development workflow, and make a
new deployment. The central question is the same as on day one: **do you
understand what you built?**

## Assignments

- [01 — Start building with an AI assistant](01-start-building-with-ai.md)

Later assignments will appear here when their requirements are introduced in
class.
