from dotenv import load_dotenv
load_dotenv()                       # pulls values from .env

import os
import pandas as pd
import phoenix as px
from phoenix.experiments import run_experiment
from src.retriever import find_similar_wineries

# ── build a tiny in-memory dataset ────────────────────────────────────
df = pd.DataFrame({"user_query": [
    "I’m hunting bold red-wine spots under $30 per tasting",
    "Sweet-white tastings for a family of six, max $20",
    "Boutique wineries for two, budget is $40",
    "Need Zinfandel-focused stops for 12 people, $35 cap",
    "Love Rhône-style reds, group of 4, keep it under $25",
]})

# ── create a Phoenix client that targets Cloud ────────────────────────
client = px.Client(endpoint="https://team5-phoenix.xyz")                    # reads PHOENIX_HOST & API key automatically
#      └─ if you prefer to be explicit:
# client = px.Client(endpoint=os.getenv("PHOENIX_HOST"))

dataset = client.upload_dataset(
    dataframe=df,
    input_keys=["user_query"],
    output_keys=[],
    dataset_name="wine-rag-queries-v12",
)

def retrieval_task(input):
    rows = find_similar_wineries(input["user_query"])        # already traced
    return {"docs": [r[0] for r in rows]}           # JSON-serialisable

# dummy retrieval task for testing
# def retrieval_task(user_query: str):
#     """Return a predictable, JSON-serialisable result.

#     • No database calls
#     • No OpenAI calls
#     • No tracing spans
#     """
#     return {"docs": [f"dummy-doc-for-{user_query}"]}

exp = run_experiment(
    dataset=dataset,
    task=retrieval_task,
    experiment_name="retriever_v12",
)

print("View results ➜", exp.url)