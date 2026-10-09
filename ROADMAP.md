# Course roadmap

This is an instructor planning note. Published assignments define the current
student requirements. Later topics and assignment numbers can still change.

## Next: Assignment 11 — Document lookup

Extend the existing game assistant with tools that search and read approved local
Markdown help, rules and lore. Build on Assignment 10's tool loop with a small,
visible implementation, such as keyword search and reading selected sections.
Keep sources traceable and access limited to documents the player may see.
Discuss the exact experiment and integration requirements before authoring.

Keep this assignment focused on document lookup through custom tools. It will
not introduce MCP, RAG theory, embeddings or vector databases.

## Dedicated assignments later

- **Model Context Protocol (MCP):** give the protocol a full explanation and its
  own assignment. It is removed from Assignment 10. Timing and scope are undecided,
  probably much later in the course.
- **Retrieval-augmented generation (RAG), embeddings and vector databases:** give
  these connected topics a dedicated assignment rather than a theory sidebar in
  Assignment 11. Timing, tooling and practical scope remain to be decided.

After the current application-LLM sequence, the planned operational progression
is automated testing and continuous integration, Docker Compose and production
deployment with continuous delivery, then Prometheus/Grafana monitoring if time
allows. The placement of the dedicated MCP and RAG assignments is still open.
