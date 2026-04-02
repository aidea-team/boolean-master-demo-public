# Boolean Master Demo Sessions

## Overview

This repository supports three one and a half hour online demo sessions that serve as a preview for a five-to-six-month AI engineering course. The audience consists of 1,000-2,000 developers who can code but have limited AI experience. Because of the audience size and broadcast format, engagement is limited — the sessions are primarily demonstrations, not hands-on workshops.

All three sessions share a common thread: **a dataset of recipes**. Each session builds on concepts from the previous one, so attendees are expected to have seen prior sessions.

This repo houses the code for **Session 1**.

### Key considerations

- **Over-prepare**: With a large, mostly passive audience and limited interaction, running out of material is the biggest risk. Always have backup demos and deeper dives ready.
- **Principles over code**: Since attendees won't replicate the code live, focus on architecture, general principles, and visual explanations (Mermaid diagrams) alongside the actual implementation.
- **Sequential**: Each session assumes familiarity with the previous one.

---

## Session 1 — LLM-Based Recipe Processing

**Goal**: Use LLMs to extract structured data from raw recipe text — ingredients, cooking techniques, times, etc. This is about using LLMs as processing tools, not building a chatbot.

### Structure

1. **Present the problem**: Raw recipe text is messy and unstructured. The goal is to get clean, structured data out of it.
2. **Explain the approach**: Why LLMs are the right tool. What makes a good prompt. What good structured output looks like.
3. **Show the architecture**: Mermaid diagram of the pipeline — raw recipe text in, prompt design, LLM reasoning, structured JSON out.
4. **Live demo**: Run the extraction code on several recipes, show the clean output.

### Backup material

- Multiple recipes of varying complexity (simple, complex, edge cases).
- Comparison of different prompting strategies and their impact on output quality.
- Before-and-after: naive vs. well-designed prompts.
- Diagrams comparing prompt strategies side-by-side.

---

## Session 2 — RAG System

**Goal**: Build a vector database of recipes and a chatbot that can retrieve and answer questions about them using retrieval-augmented generation.

### Structure

1. **Motivate the problem**: "What if someone wants to ask questions about recipes, not just extract data?"
2. **Explain the components**: Embeddings, vector storage, semantic search, and why it beats keyword search.
3. **Show the architecture**: Mermaid diagram of the RAG pipeline — user query to embedding, vector similarity search, top results fed into the LLM for response generation.
4. **Live demo**: Query the system (e.g., "what can I make with tomatoes and basil?"), show retrieval and chatbot response.

### Backup material

- Queries of varying difficulty.
- Comparison of retrieval with and without reranking.
- Different embedding models and their trade-offs.

---

## Session 3 — Agentic Capabilities

**Goal**: Extend the RAG chatbot with function calling so the agent can take actions in the external world, not just retrieve and respond.

### Structure

1. **Motivate the problem**: "What if your recipe assistant could actually do something, not just tell you?"
2. **Introduce function calling**: The agent sees available tools, reasons about which to use, calls them, and acts on the results.
3. **Show the architecture**: Mermaid diagram of the agent loop — user query, agent reasoning, function selection, execution, result handling, response.
4. **Live demo**: The agent takes an action that is visible in an external system (e.g., creating a recipe card or shopping list in Notion, or calling an external API like Open Food Facts to enrich recipes with real nutritional data).

### Integration options (under consideration)

- **Notion**: Agent creates recipe cards or meal plans in a Notion database. Visual, persistent, recognizable. Auth is straightforward.
- **Open Food Facts API**: Free, no auth. Agent looks up real products by name/barcode to get nutrition data, allergens, Nutriscore. Useful for enriching a shopping list with real market data.
- **Trello / Discord**: Lighter alternatives for visible external actions.

The key requirement: the integration must have an existing frontend so the audience can see the agent's action reflected in a real tool, and authentication must be simple enough for a reliable live demo.

### Backup material

- Multiple scenarios triggering different function calls.
- Sequential function calls (agent chains actions).
- Edge cases and constraint handling.
