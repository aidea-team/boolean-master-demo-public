---
theme: penguin
title: Lavorare con i Dati Usando l'AI — Lezione 2
layout: intro
transition: slide-left
comark: true
duration: 60min
themeConfig:
  logoHeader: ''
  eventLogo: ''
  eventUrl: ''
---

# Lavorare con i Dati Usando l'AI

Lezione 2 — Dal vector database all'agente

<!--
Totale 60'. Scaletta: 0-5 recap, 5-20 vector DB, 20-30 RAG, 30-55 agente, 55-60 chiusura.
-->

---
layout: presenter
presenterImage: /federico_romeo_cropped.png
---

# Chi sono

### Federico Romeo

- AI Engineer presso **aidea**
- Docente per **Boolean**

---
layout: new-section
---

# Dove eravamo rimasti

---
layout: default
---

# La volta scorsa

<v-clicks>

- Abbiamo usato un LLM per trasformare **testo grezzo di ricette** in **JSON strutturato**
- Abbiamo visto che la **ricerca per keyword** confronta parole, non significato
- Abbiamo trasformato 1.000 ricette in **embeddings**: un vettore di 1.536 numeri per ricetta
- Con la **cosine similarity** abbiamo cercato per significato

</v-clicks>

<br>

<v-click>

| Query | Keyword | Semantica |
|---|---|---|
| `"dish with marinara"` | solo le ricette con la parola "marinara" | anche quelle con salsa di pomodoro |
| `"quick weeknight dinner"` | **zero risultati** | piatti veloci e semplici |

</v-click>

<!--
5 minuti al massimo. Il pubblico ha visto embeddings e cosine similarity con NumPy (session2/segment_1): non rifarlo, richiamalo.
-->

---
layout: default
---

# Il piano di oggi

Prendiamo la ricerca semantica e la facciamo diventare un **agente** che agisce nel mondo reale.

<br>

```mermaid {theme: 'base', themeVariables: {primaryColor: '#2B4162', primaryTextColor: '#2B4162', lineColor: '#5FA8D3', secondaryColor: '#E8F1F2', tertiaryColor: '#f5f5f5'}, scale: 0.9}
flowchart LR
    A["1. Vector database<br/>cercare in modo scalabile"] --> B["2. RAG<br/>rispondere con dati reali"]
    B --> C["3. Agente<br/>decidere e agire"]

    style A fill:#E8F1F2,stroke:#2B4162,color:#2B4162
    style B fill:#5FA8D3,stroke:#2B4162,color:#fff
    style C fill:#2B4162,stroke:#2B4162,color:#fff
```

<br>

<v-click>

Il filo conduttore resta lo stesso: **le nostre 1.000 ricette**.

</v-click>

---
layout: new-section
---

# Perché ci serve un vector database?

<!--
Blocco vector DB: 15 minuti, fino al minuto 20.
-->

---
layout: default
---

# NumPy funziona, ma...

La volta scorsa abbiamo calcolato la cosine similarity con NumPy: su 1.000 ricette va benissimo.

<br>

<v-clicks>

Ma con **100.000 ricette**? O **1 milione**?

- Ogni query confronta **tutti** i vettori → O(n)
- Tutti i vettori devono stare **in memoria**
- Nessuna persistenza: gli embedding si perdono quando il notebook si riavvia
- Nessun filtro (es. "solo ricette vegetariane")

</v-clicks>

<br>

<v-click>

Un **vector database** risolve tutto questo:

- Algoritmi di **Approximate Nearest Neighbor** (ANN) → veloce anche su larga scala
- **Storage persistente**: i dati sopravvivono ai riavvii
- **Filtri sui metadati**: combina ricerca semantica e filtri

</v-click>

---
layout: default
---

# Come fa a essere veloce?

Invece di confrontare la query con **ogni** vettore, il database costruisce un **indice**.

<br>

<v-clicks>

- L'indice più usato si chiama **HNSW**: un grafo in cui ogni vettore è collegato ai suoi vicini
- La ricerca parte da un punto e **salta di vicino in vicino**, sempre verso la query
- Pochi salti invece di milioni di confronti

</v-clicks>

<br>

<v-click>

Il prezzo: è **approssimato**. Ogni tanto può perdere il vicino esatto.

In cambio risponde in **millisecondi** su milioni di vettori: per la ricerca semantica è un ottimo affare.

</v-click>

<!--
Analogia: chiedere la strada. Non controlli tutte le vie della città, chiedi a chi è vicino e ti avvicini a ogni passo.
-->

---
layout: default
---

# Qdrant

Useremo **Qdrant**, un vector database open-source.

<v-clicks>

- Si avvia in locale con un singolo `docker compose up`
- Ha una **dashboard web** su `localhost:6333/dashboard`
- Il client Python è semplice e intuitivo

</v-clicks>

<v-click>

Tre concetti:

| Qdrant | Equivalente "classico" | Nel nostro caso |
|---|---|---|
| **Collection** | una tabella | `recipes` |
| **Point** | una riga | una ricetta |
| **Vector** | la colonna su cui si cerca | l'embedding della ricetta |
| **Payload** | le altre colonne | titolo, ingredienti, istruzioni |

</v-click>

---
layout: new-section
---

# Proviamolo

notebook `session2/segment_2.ipynb` — Qdrant

<!--
Mostrare la dashboard su localhost:6333/dashboard dopo l'inserimento.
-->

---
layout: new-section
---

# Dalla ricerca all'assistente

<!--
Blocco RAG: 10 minuti, fino al minuto 30.
-->

---
layout: default
---

# E se un LLM rispondesse usando le nostre ricette?

Ora abbiamo una funzione che prende una query e restituisce le ricette più rilevanti.

<br>

<v-clicks>

1. L'utente chiede: *"Cosa posso cucinare con il pollo avanzato?"*
2. Trasformiamo la domanda in embedding e cerchiamo in Qdrant
3. Prendiamo le **5 ricette più rilevanti**
4. Le passiamo all'LLM come **contesto**, insieme alla domanda

</v-clicks>

<br>

<v-click>

Questo pattern si chiama **RAG**, Retrieval-Augmented Generation.

L'LLM non inventa: prima **recupera** dati reali, poi **genera** una risposta basata su quei dati.

</v-click>

---
layout: default
---

# L'architettura

```mermaid {theme: 'base', themeVariables: {primaryColor: '#2B4162', primaryTextColor: '#2B4162', lineColor: '#5FA8D3', secondaryColor: '#E8F1F2', tertiaryColor: '#f5f5f5'}, scale: 0.75}
flowchart LR
    A["Domanda"] --> B["Embedding"]
    B --> C[("Qdrant")]
    C -->|"top 5"| D["Prompt<br/>domanda + ricette"]
    D --> E["LLM"]
    E --> F["Risposta"]

    style A fill:#E8F1F2,stroke:#2B4162,color:#2B4162
    style B fill:#5FA8D3,stroke:#2B4162,color:#fff
    style C fill:#5FA8D3,stroke:#2B4162,color:#fff
    style D fill:#E8F1F2,stroke:#2B4162,color:#2B4162
    style E fill:#2B4162,stroke:#2B4162,color:#fff
    style F fill:#E8F1F2,stroke:#2B4162,color:#2B4162
```

<br>

<v-click>

Qui siamo **noi** a decidere quando cercare: a ogni domanda, sempre.

</v-click>

---
layout: new-section
---

# Costruiamolo

notebook `session2/segment_3.ipynb` — RAG

---
layout: new-section
---

# Il limite del nostro assistente

<!--
Blocco agente: 25 minuti, fino al minuto 55.
-->

---
layout: default
---

# Il problema: nessun contesto

Nel RAG che abbiamo appena costruito, **eravamo noi** a chiamare `retrieve_recipes()`.

<br>

Ogni query era **indipendente**: il sistema non aveva memoria.

<v-clicks>

- Turno 1: *"Cerco una ricetta con il pesce"* → funziona!
- Turno 2: *"Dammene un'altra"* → ???

</v-clicks>

<br>

<v-click>

"Dammene un'altra" viene embeddata **alla lettera**, e il vector database non sa di cosa stessimo parlando.

Vediamolo in pratica.

</v-click>

---
layout: new-section
---

# Vediamolo

notebook `session3/segment_1.ipynb` — il limite del loop naive

---
layout: new-section
---

# Function Calling

---
layout: default
---

# E se l'LLM potesse usare strumenti?

Finora l'LLM riceveva testo e rispondeva con testo.

<br>

Con il **function calling**, l'LLM può fare qualcosa di nuovo:

<v-clicks>

- Vede una lista di **tool disponibili** (funzioni che può chiamare)
- Analizza la richiesta dell'utente
- **Decide da solo** se e quale tool usare
- Restituisce una **richiesta strutturata** (JSON) per eseguire il tool

</v-clicks>

<br>

<v-click>

L'LLM **non esegue** il codice: chiede a noi di farlo.
Noi eseguiamo, restituiamo il risultato, e l'LLM genera la risposta finale.

</v-click>

---
layout: default
---

# Il loop agentico

```mermaid {theme: 'base', themeVariables: {primaryColor: '#2B4162', primaryTextColor: '#2B4162', lineColor: '#5FA8D3', secondaryColor: '#E8F1F2', tertiaryColor: '#f5f5f5'}, scale: 0.85}
flowchart LR
    A["Utente"] -->|"query"| B["LLM"]
    B -->|"tool_call"| C["retrieve_recipes"]
    C -->|"risultati"| D["LLM"]
    D --> E["Risposta"]

    style A fill:#E8F1F2,stroke:#2B4162,color:#2B4162
    style B fill:#2B4162,stroke:#2B4162,color:#fff
    style C fill:#5FA8D3,stroke:#2B4162,color:#fff
    style D fill:#2B4162,stroke:#2B4162,color:#fff
    style E fill:#E8F1F2,stroke:#2B4162,color:#2B4162
```

<v-click>

Il contesto della conversazione viene **mantenuto**: "dammene un'altra" ora funziona.

È la stessa ricerca di prima, ma ora a decidere **quando** e **cosa** cercare è l'LLM.

</v-click>

---
layout: new-section
---

# Proviamolo

notebook `session3/segment_2.ipynb` — function calling

---
layout: new-section
---

# Dall'assistente all'agente

---
layout: default
---

# Ok, cerca ricette. Ma se potesse anche *agire*?

Finora il nostro agente può solo **cercare** ricette e **rispondere**.

<br>

E se potesse anche **fare qualcosa nel mondo reale**?

<v-clicks>

- Trovare una ricetta
- Estrarne gli ingredienti
- **Creare una lista della spesa** su Trello, automaticamente

</v-clicks>

<br>

<v-click>

Basta aggiungere un secondo tool. L'agente **decide da solo** la sequenza:

1. Cerca la ricetta con `retrieve_recipes`
2. Aggiunge gli ingredienti con `add_to_shopping_list`

</v-click>

---
layout: default
---

# L'architettura

```mermaid {theme: 'base', themeVariables: {primaryColor: '#2B4162', primaryTextColor: '#2B4162', lineColor: '#5FA8D3', secondaryColor: '#E8F1F2', tertiaryColor: '#f5f5f5'}, scale: 0.85}
flowchart LR
    A["Utente"] -->|"query"| B["LLM"]
    B -->|"tool_call"| C[("Qdrant")]
    C -->|"ricette"| D["LLM"]
    D -->|"tool_call"| E[("Trello")]
    E --> F["Risposta"]

    style A fill:#E8F1F2,stroke:#2B4162,color:#2B4162
    style B fill:#2B4162,stroke:#2B4162,color:#fff
    style C fill:#5FA8D3,stroke:#2B4162,color:#fff
    style D fill:#2B4162,stroke:#2B4162,color:#fff
    style E fill:#0079BF,stroke:#2B4162,color:#fff
    style F fill:#E8F1F2,stroke:#2B4162,color:#2B4162
```

---
layout: new-section
---

# Costruiamolo

notebook `session3/segment_3.ipynb` — integrazione Trello

<!--
Tenere aperta la board: https://trello.com/b/GAinQpED/lista-della-spesa
-->

---
layout: new-section
---

# Cosa abbiamo costruito

<!--
Chiusura: 5 minuti.
-->

---
layout: default
---

# Da testo grezzo ad agente autonomo

<v-clicks>

**La volta scorsa**: LLM e ricerca semantica
- Testo grezzo → dati strutturati (JSON)
- Testo → vettori → ricerca per significato

**Oggi**: dal database all'agente
- Vector database: la ricerca semantica in modo scalabile
- RAG: risposte basate su dati reali
- Function calling: l'LLM decide quali tool usare
- Integrazione con il mondo reale (Trello): da "risponde" ad "agisce"

</v-clicks>

<br>

<v-click>

Il pattern è sempre lo stesso: **dare all'LLM gli strumenti giusti e lasciarlo ragionare**.

</v-click>

---
layout: new-section
---

# Grazie!

Domande?
