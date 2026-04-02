# Boolean Master Demo

Code and materials from the Boolean Master demo series — three live sessions introducing AI engineering concepts to developers, using a recipe dataset as a common thread.

## Sessions

| Session | Topic | Description |
|---------|-------|-------------|
| 1 | LLM-Based Recipe Processing | Using LLMs to extract structured data from raw recipe text |
| 2 | RAG System | Building a vector database of recipes and a retrieval-augmented chatbot |
| 3 | Agentic Capabilities | Extending the chatbot with function calling to take actions in external systems |

Each session folder contains:
- **Jupyter notebooks** (`segment_1.ipynb`, `segment_2.ipynb`, `segment_3.ipynb`) — the demo code
- **slides.pdf** — the presentation slides
- **requirements.txt** — Python dependencies

Sessions 2 and 3 also include a `docker-compose.yml` for required services.

See [SESSIONS.md](SESSIONS.md) for a detailed overview of each session's goals and structure.

## Setup

1. Create a virtual environment and install dependencies for the session you want to run:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r session1/requirements.txt
   ```

2. Copy `.env_example` to `.env` and fill in your API keys:

   ```bash
   cp .env_example .env
   ```

3. Open the notebooks in Jupyter and follow along.
