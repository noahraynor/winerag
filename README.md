# WineRag 🍷🤖

A Retrieval-Augmented Generation (RAG) application that helps plan wine tours in Paso Robles.

Built with:
- Python
- OpenAI API
- PostgreSQL
- FAISS
- Pandas

## Setup

See `requirements.txt` and `.env` for configuration.

--ingest.py
The one-time “data loader” for WineRag. It reads the paso_robles_wineries_with_specialties.csv file with pandas, builds a single descriptive sentence for each winery (name + specialties + address + group-size + tasting price), and sends that sentence to OpenAI’s text-embedding-3-small model. The returned 1 ,536-dimension vector is added as the embedding column, while the raw fields (name, address, max group size, tasting price, specialties) are inserted unchanged into their respective columns of the winery_vectors table. The result is one PostgreSQL/pgvector row per winery that contains both human-readable metadata and a machine-readable semantic fingerprint—allowing later queries to filter on price or group size and rank results by cosine similarity to the user’s request, all in a single SQL statement.

--llm_query.py
WineRag’s “natural-language translator.” It loads your OpenAI key, wraps the GPT-4o model with the Instructor library, and exposes parse_user_query(). Given any free-form sentence (“We’re a group of six on a budget, love Rhône reds”), the function sends a single chat completion that’s constrained by your WinerySearchRequest Pydantic schema and enriched by a developer prompt that defines sensible defaults. Instructor validates the response and returns a fully-typed object containing query, max_price, and min_group_size. All later layers—the retriever, Gradio UI, CLI—consume this structured request instead of raw text, letting them combine precise SQL filters with semantic vector search.

-- retriever.py
WineRag’s “search engine.” It takes raw user text, uses parse_user_query() to turn that text into a validated WinerySearchRequest, embeds the request’s query with OpenAI’s text-embedding-3-small, and then runs a single Postgres query that combines pgvector cosine-similarity ranking with classic SQL filters for tasting price and group size. The script returns the top N wineries (default four) sorted by similarity, handing back full metadata—name, address, group capacity, price, specialties—plus a similarity score. Both the CLI and Gradio UI call this one function, so you have a single source of truth for semantic search and numeric filtering.
