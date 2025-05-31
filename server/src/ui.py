# ui.py
import gradio as gr
from .llm_query import parse_user_query
from .retriever import find_similar_wineries

def handle_query(user_input):
    try:
        results = find_similar_wineries(user_input)
        formatted = ""
        for winery in results:
            name, address, group_size, price, specialties, similarity = winery
            formatted += f"""
🏷️ {name} ({similarity:.2f} similarity)
📍 {address}
👥 Max group size: {group_size}
💵 Tasting price: ${price}
🍷 Specialties: {specialties}

---
"""
        return formatted.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

iface = gr.Interface(
    fn=handle_query,
    inputs=gr.Textbox(label="Describe your perfect wine tour"),
    outputs=gr.Textbox(label="Wine Tour Options"),
    title="🍷 WineRag Tour Planner",
    description="Plan your wine tour using natural language. We'll match you with the best wineries in Paso Robles!"
)

if __name__ == "__main__":
    iface.launch()
