import pandas as pd
import psycopg2
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
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

# Read winery data from CSV
df = pd.read_csv("data/paso_robles_wineries_with_specialties.csv")

# Connect to PostgreSQL
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# Loop through each winery
for _, row in df.iterrows():
    text = f"{row['Winery Name']} offers {row['Wine Specialties']} at {row['Address']}. Max group size {row['max group size']}. Tasting price ${row['Tasting Price']}."
    
    # Create embedding
    embedding_response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    embedding = embedding_response.data[0].embedding  # This is a list of floats

    # Insert into DB
    cursor.execute("""
        INSERT INTO winery_vectors (name, address, group_size, tasting_price, specialties, embedding)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        row['Winery Name'],
        row['Address'],
        int(row['max group size']),
        int(row['Tasting Price']),
        row['Wine Specialties'],
        embedding  # psycopg2 + pgvector supports this as a Python list
    ))

# Commit + close
conn.commit()
cursor.close()
conn.close()

print("Winery data loaded and embedded successfully.")