from langchain_openai import ChatOpenAI
from src.calls.main import create_agent, invoke_agent
from src.calls.tools.think import think
from src.calls.constants import API_KEY, SERPER_API_KEY
from typing import List
import streamlit as st
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import Tool


# Define the task for generating existing alternatives
TASK = "Identify existing alternatives for the given problem and customer segments. Make sure to use both tools at least once. Provide a bullet-point list of these alternatives."


search = GoogleSerperAPIWrapper(
        serper_api_key=SERPER_API_KEY
    )



# Initialize the tools
tools = [
    think,
        Tool(
        name="search-tool",
        func=search.run,
        description="useful for when you need to search any information.",
    )
]

# Set up the language model
llm = ChatOpenAI(
    api_key=API_KEY,
    model="gpt-4o-mini",
    temperature=0.7
)

# Create the agent
agent = create_agent(
    llm,
    tools,
    TASK
)

def generate_existing_alternatives(
    problem: str,
    customer_segments: str
) -> str:
    """
    Generate a list of existing alternatives based on the given problem and customer segments.

    Args:
        problem (str): The problem statement.
        customer_segments (str): A description of customer segments.

    Returns:
        List[str]: A list of existing alternatives.
    """
    # Display a message in the Streamlit app
    st.markdown("## Identifying existing alternatives..")
    
    # Invoke the agent with the problem and customer segments
    response = invoke_agent(agent, {
        "problem": problem,
        "customer_segments": customer_segments
    })
    return response 