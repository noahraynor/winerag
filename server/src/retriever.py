import os
import psycopg2
from dotenv import load_dotenv
from openai import OpenAI

# import langsmith as ls                        # NEW ← gives get_current_run_tree
# from langsmith import wrappers, traceable

from src.llm_query import parse_user_query
from src.search_models import WinerySearchRequest

# ── env & clients ───────────────────────────────────────────────────────
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "dbname": os.getenv("DB_NAME"),
}

client = OpenAI(api_key=API_KEY)

# ── helpers ─────────────────────────────────────────────────────────────
def embed_query(text: str):
    response = client.embeddings.create(
        input=[text], model="text-embedding-3-small"
    )
    return response.data[0].embedding

                                  # root span
def find_similar_wineries(
    user_input: str, limit: int = 4, min_similarity: float = 0.3
):
    parsed: WinerySearchRequest = parse_user_query(user_input)
    print("\nParsed user input:", parsed)

    embedding = embed_query(parsed.query)

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    sql = """
    SELECT
        name, address, group_size, tasting_price, specialties,
        1 - (embedding <=> %s::vector) AS similarity
    FROM winery_vectors
    WHERE 1 - (embedding <=> %s::vector) > %s
    """
    params = [embedding, embedding, min_similarity]

    if parsed.max_price:
        sql += " AND tasting_price <= %s"
        params.append(parsed.max_price)

    if parsed.min_group_size:
        sql += " AND group_size >= %s"
        params.append(parsed.min_group_size)

    sql += " ORDER BY similarity DESC LIMIT %s"
    params.append(limit)

    cursor.execute(sql, tuple(params))
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    print(results)
    return results


# ── CLI entry point ────────────────────────────────────────────────────
if __name__ == "__main__":
    request_message = """
    What type of wine tour are you planning?
    I can account for your wine preferences, group
    size, and budget.
    """

    query = input(request_message)
    rows = find_similar_wineries(query)

    print("\nHere are your suggested wineries:")
    for name, address, group_size, price, specialties, sim in rows:
        print(
            f"""
🏧 {name} ({sim:.2f} similarity)
📍 {address}
👥 Max group size: {group_size}
💵 Tasting price: ${price}
🍷 Specialties: {specialties}
"""
        )
