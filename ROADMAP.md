# Course roadmap

Updated 9 October 2026.

This is an instructor planning note. Published assignments define the current
student requirements. Later topics and assignment numbers can still change.

## Current status

Assignments **01–11 are published on main**. See the [assignment list](README.md#assignments).
The game-chat screenshot for Assignment 10 is included. Assignment 11 screenshots
and any remaining walkthrough feedback are pending. After those are incorporated,
course authoring will pause until the instructor resumes it.
Assignment 12's direction is agreed, but it has not been written. Production
infrastructure is also deferred.

## Published: Assignment 11 — Document lookup

[Assignment 11](11-let-your-game-assistant-look-up-documents.md) extends the existing
game chat with tools that search and read approved Markdown help, rules and lore.
It uses simple keyword search and selected sections, with traceable sources and
player access checks. Theory and diagrams lead directly into game integration,
without a separate starter script or terminal experiment.
A short optional section introduces SQL queries, full-text indexing and knowledge
graphs as alternative ways to organize and retrieve information. No additional
implementation or infrastructure is required.

It focuses on document lookup through custom tools. MCP, RAG theory, embeddings
and vector databases are reserved for dedicated later assignments.

## Agreed next: Assignment 12 — Automated tests and CI

Help students build a small, useful safety net for their existing game with their
coding agent. Keep the scope focused rather than surveying every testing technique.

1. Choose meaningful behavior to protect, such as a game rule, player permissions
   or an important backend endpoint.
2. Build tests and understand their setup, action and expected result.
3. Introduce a small regression, see a test fail, then fix it and see it pass.
4. Run the same checks in GitHub Actions and introduce a simple branch, pull request,
   checks, review and merge workflow.

Use predictable example model responses for normal application tests. Test tool
dispatch, permissions and document lookup without calling the school model on every
CI run. Assessing live model answers is a separate concern. CI can use GitHub-hosted
runners, so this assignment does not require the future production machine.

Afterwards, teach Docker/Compose, a repeatable deployment to a separate production
host, then continuous deployment and Prometheus/Grafana monitoring if time allows.
Resolve production access, configuration, secrets and persistent data before
automating deployment. Exact assignment grouping after 12 remains open.

## Dedicated assignments later

- **Model Context Protocol (MCP):** give the protocol a full explanation and its
  own assignment. It is removed from Assignment 10. Timing and scope are undecided,
  probably much later in the course.
- **Retrieval-augmented generation (RAG), embeddings and vector databases:** give
  these connected topics a dedicated assignment rather than a theory sidebar in
  Assignment 11. Timing, tooling and practical scope remain to be decided.

The placement of the dedicated MCP and RAG assignments is still open.
