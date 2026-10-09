# Course roadmap

This is an instructor planning note. Published assignments define the current
student requirements. Later topics and assignment numbers can still change.

## Assignment 11 — Document lookup

Extend the existing game assistant with tools that search and read approved local
Markdown help, rules and lore. Build on Assignment 10's tool loop with a small,
visible implementation, such as keyword search and reading selected sections.
Keep sources traceable and access limited to documents the player may see.
Teach the theory first, then guide students directly through integration into
their existing game chat. No separate starter script or terminal experiment.
Use diagrams to explain selecting context, searching and reading sections, and
combining documentation with live game state.

Keep this assignment focused on document lookup through custom tools. It will
not introduce MCP, RAG theory, embeddings or vector databases.

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

## Current checkpoint

Finish the instructor's walkthrough feedback and screenshots for Assignments 10
and 11, then pause course authoring. The Assignment 12 direction is agreed, but
writing it and provisioning production infrastructure are deferred until the
instructor explicitly resumes the project.

## Dedicated assignments later

- **Model Context Protocol (MCP):** give the protocol a full explanation and its
  own assignment. It is removed from Assignment 10. Timing and scope are undecided,
  probably much later in the course.
- **Retrieval-augmented generation (RAG), embeddings and vector databases:** give
  these connected topics a dedicated assignment rather than a theory sidebar in
  Assignment 11. Timing, tooling and practical scope remain to be decided.

The placement of the dedicated MCP and RAG assignments is still open.
