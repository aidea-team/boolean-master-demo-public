# Lezione 2 — Dal vector database all'agente

Una lezione da 60 minuti che riparte da dove si è fermata la prima: embeddings e cosine
similarity con NumPy (`session2/segment_1.ipynb`) sono già stati fatti.

Slide: `lezione2/slides.pdf` (sorgente Slidev in `lezione2/slidev-deck/`).

## Scaletta

| Minuti | Blocco | Slide | Notebook |
|---|---|---|---|
| 0–5 | Chi sono, recap, piano di oggi | 1–5 | — |
| 5–20 | Vector database: perché, HNSW, Qdrant | 6–10 | `session2/segment_2.ipynb` |
| 20–30 | RAG | 11–14 | `session2/segment_3.ipynb` |
| 30–55 | Il limite del loop naive, function calling, agente con Trello | 15–25 | `session3/segment_1.ipynb`, `segment_2.ipynb`, `segment_3.ipynb` |
| 55–60 | Recap e domande | 26–28 | — |

## Prima della lezione

1. Qdrant acceso: `cd session3 && docker compose up -d` (dashboard su http://localhost:6333/dashboard).
   La collection `recipes` la ricrea comunque `session2/segment_2.ipynb`.
2. VS Code: `code .` dalla root della repo, kernel `.venv/bin/python` per tutti i notebook.
3. `.env` nella root con `OPENAI_API_KEY`, `TRELLO_API_KEY`, `TRELLO_TOKEN`, `TRELLO_LIST_ID`.
4. Board Trello vuota: `.venv/bin/python lezione2/reset_trello.py --yes`.
5. Board aperta in un tab: https://trello.com/b/GAinQpED/lista-della-spesa

## Chiave e token Trello

Già fatto il 3/11/2026: app "Boolean demo" nel workspace *aidea*, token senza scadenza (read, write),
entrambi nel `.env`. Se servisse rigenerarli:

1. https://trello.com/power-ups/admin → **New** → un Power-Up nel workspace *aidea*
   (nome a piacere, es. "Boolean demo"; l'iframe URL può restare vuoto).
2. Tab **API key** → **Generate a new API key** → copiala in `TRELLO_API_KEY`.
3. Accanto alla key, il link **Token** (oppure apri
   `https://trello.com/1/authorize?expiration=never&scope=read,write&response_type=token&name=Boolean%20demo&key=<API_KEY>`)
   → **Allow** → copia il token in `TRELLO_TOKEN`.

## Rigenerare il PDF

```bash
cd lezione2/slidev-deck
npm install          # solo la prima volta
npm run export       # scrive lezione2/slides.pdf
```
