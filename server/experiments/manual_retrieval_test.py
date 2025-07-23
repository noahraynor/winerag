# experiments/manual_retrieval_test.py

from dotenv import load_dotenv
load_dotenv()

from src.retriever import find_similar_wineries

queries = [
    "I’m hunting bold red-wine spots under $30 per tasting",
    "Sweet-white tastings for a family of six, max $20",
    "Boutique wineries for two, budget is $40",
    "Need Zinfandel-focused stops for 12 people, $35 cap",
    "Love Rhône-style reds, group of 4, keep it under $25",
]

for i, query in enumerate(queries, start=1):
    print(f"\n🔍 Test {i}: {query}")
    results = find_similar_wineries(query)
    for name, address, group_size, price, specialties, sim in results:
        print(f"""
🏧 {name} ({sim:.2f} similarity)
📍 {address}
👥 Max group size: {group_size}
💵 Tasting price: ${price}
🍷 S
""")
        

