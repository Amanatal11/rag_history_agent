# Ethiopian History RAG Assistant

A lightweight Retrieval-Augmented Generation (RAG) application that answers questions about Ethiopian history using a local text corpus, a persistent Chroma vector database, and a Groq-hosted LLM. The project ships with a Streamlit UI and an optional CLI.

## Features
- Ingest `.txt` sources from `data/`, chunk and embed them with `sentence-transformers/all-MiniLM-L6-v2`.
- Persist embeddings in Chroma (`chroma_db/`) for fast reloads.
- Retrieve top-k relevant chunks via semantic similarity with deduplication and thresholding.
- Build a concise, source-aware prompt for the LLM.
- Generate succinct answers using `langchain_groq.ChatGroq` authenticated via `GROQ_API_KEY`.
- Streamlit UI and CLI entry points.

## Architecture
- `app.py`: Streamlit UI for querying and displaying answers.
- `vectordb_and_ingestion.py`: `VectorDBManager` handles chunking, embedding, persistence, and retrieval.
- `prompt_builder.py`: Builds compact prompts from retrieved chunks with minimal source hints.
- `retrieval_and_response.py`: CLI pipeline mirroring the app (load/ingest → retrieve → prompt → answer).
- `logger.py`: Minimal console logger shared across modules.
- `wiki_fetcher.py`: Helper to fetch Wikipedia pages into `data/` as `.txt`.

## Prerequisites
- Python 3.12+
- A Groq API key

## Quickstart
```bash
# 1) Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Configure environment
# Create .env and set GROQ_API_KEY
printf "GROQ_API_KEY=your_key_here\n" > .env

# 4) (Optional) Seed/expand the corpus with Wikipedia content
python -c "from wiki_fetcher import fetch_and_save_page; fetch_and_save_page('Axum Empire')"

# 5) Run the Streamlit app
streamlit run app.py
```

## Screenshots

Answer found from context 
(<img width="800" height="608" alt="Screenshot from 2025-10-01 11-32-50" src="https://github.com/user-attachments/assets/392a5dbd-ae5e-4934-8edb-6e8e3b79a805" />

Answer not found (out-of-scope question):

<img width="800" height="608" alt="Screenshot from 2025-10-01 11-34-15" src="https://github.com/user-attachments/assets/baa4041e-a550-4e3a-b891-e3f3b60bb599" />


### CLI Usage
```bash
python retrieval_and_response.py "Who was Menelik II?" --top_k 2 --threshold 0.7
```

## Environment Variables
- `GROQ_API_KEY`: Your Groq API key for `langchain_groq.ChatGroq`.

Example `.env`:
```bash
GROQ_API_KEY=your_key_here
```

## Data & Persistence
- Place `.txt` sources in `data/`.
- On first run, the app/CLI will chunk, embed, and persist a Chroma collection under `chroma_db/`.
- Subsequent runs load the existing DB for faster startup.

## End-to-End Flow
1. Load (or build) the Chroma vector database via `VectorDBManager`.
2. Perform a similarity search for the query to get candidate chunks.
3. Filter by similarity threshold and remove duplicates.
4. Build a concise prompt via `prompt_builder.build_prompt`.
5. Generate an answer using `langchain_groq.ChatGroq` and return it to the UI/CLI.

## Project Structure
```
rag-history-agent/
├─ app.py                     # Streamlit UI
├─ retrieval_and_response.py  # CLI entry
├─ vectordb_and_ingestion.py  # VectorDBManager (chunk/embed/persist)
├─ prompt_builder.py          # Prompt assembly
├─ logger.py                  # Shared logger
├─ wiki_fetcher.py            # Wikipedia ingestion utility
├─ data/                      # Text corpus (.txt files)
├─ chroma_db/                 # Chroma persistence (ignored by git)
├─ requirements.txt           # Python dependencies
├─ .gitignore
└─ README.md
```

## Troubleshooting
- "GROQ_API_KEY missing": Ensure `.env` exists, includes `GROQ_API_KEY`, and `python-dotenv` is installed.
- Long initial startup: First run embeds the corpus; subsequent runs are faster.
- Weak answers: Increase `Top-K`, lower the `Similarity threshold`, or add more documents to `data/`.
- Dependency errors: Verify the virtual environment is active and dependencies are installed from `requirements.txt`.

## Suggested Dependencies
If `requirements.txt` isn’t populated, include:
```
streamlit
python-dotenv
langchain
langchain-community
langchain-groq
sentence-transformers
chromadb
requests
beautifulsoup4
```

## License
Provided as-is for educational purposes. Add a license of your choice for distribution or commercial use.

