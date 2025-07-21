# src/llm_query.py
import os
from dotenv import load_dotenv
from openai import OpenAI
import instructor

from .search_models import WinerySearchRequest

load_dotenv()

base_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = instructor.patch(base_client)  # schema-aware

def parse_user_query(user_input: str) -> WinerySearchRequest:
    
    developer_content = """
    You are a helpful AI bot. You are taking in a user input string and returning
    a structured WinerySearchRequest.  The query property will be the type of 
    wine that the group has a preference for.  If they don't specify, you can fill in
    red and white wine.

    The max_price represents the maximum price that the group will pay at each winery.
    If they want a cheaper experience but don't specify a price, you can fill in $20.
    If they want medium priced options, you can choose $40. If they want an expensive,
    high end experience, fill in $100 here.

    The min_group_size property represents the size of the group going on the wine tour.
    If they specify a group size, you can just fill it in here.  If they say it is a couple,
    you can fill in 2.  If they say a large group, you can set it to 10.  Try to guess the number
    of people going on the trip and fill it in here.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "developer",
            "content": developer_content
            },
                        {
            "role": "user",
            "content": user_input
            }
        ],
        response_model=WinerySearchRequest,
    )

    return response

if __name__ == "__main__":
    user_input = input("Type your wine tour query:\n> ")
    result = parse_user_query(user_input)
    print("\nStructured Query:")
    print(result)
