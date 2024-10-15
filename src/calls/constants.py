from langchain_openai import ChatOpenAI
import dotenv
import os

dotenv.load_dotenv()
CONTEXT = """
You're an expert reasoner. Together with other expert reasoners & business experts, you're generating a lean canvas for a succesful entrepeneur.
For your information: The lean canvas:

The Lean Canvas is a one-page business model framework that helps startups and entrepreneurs quickly outline their business idea. It focuses on key elements such as problem, solution, key metrics, unique value proposition, customer segments, channels, cost structure, and revenue streams. This tool encourages iterative development and emphasizes identifying and validating assumptions to foster a more agile approach to business planning.
"""

API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")