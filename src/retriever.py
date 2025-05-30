import psycopg2
from openai import OpenAI
from dotenv import load_dotenv
import os
from src.llm_query import parse_user_query
from src.search_models import WinerySearchRequest

# Load secrets from .env
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

# Function to embed the user query
def embed_query(text):
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

# Function to retrieve similar wineries using cosine similarity
def find_similar_wineries(user_input, limit=4, min_similarity=0.3):
    parsed: WinerySearchRequest = parse_user_query(user_input)
    print("\nParsed user input from instructor:", parsed)

    embedding = embed_query(parsed.query)

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    sql = """
    SELECT 
        name,
        address,
        group_size,
        tasting_price,
        specialties,
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

    return results

# Run as standalone script
if __name__ == "__main__":
    
    request_message = """
    What type of wine tour are you planning?\n
    I can account for your wine preferences, group
    size, and budget.\n
    """

    query = input(request_message)
    results = find_similar_wineries(query)

    print("\nHere are your suggested wineries:")
    for winery in results:
        name, address, group_size, price, specialties, similarity = winery
        print(f"""
🏧 {name} ({similarity:.2f} similarity)
📍 {address}
👥 Max group size: {group_size}
💵 Tasting price: ${price}
🍷 Specialties: {specialties}
""")
