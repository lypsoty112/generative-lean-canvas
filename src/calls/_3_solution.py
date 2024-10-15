from langchain_openai import ChatOpenAI
from src.calls.main import create_agent, invoke_agent
from src.calls.tools.think import think
from src.calls.constants import API_KEY
import streamlit as st

# Define the task for generating a solution
TASK = "Generate a comprehensive solution that can be built into a business for the given problem, customer segments, and existing alternatives. Provide a detailed description of the solution."

# Initialize the language model
llm = ChatOpenAI(
    api_key=API_KEY,
    model="gpt-4o-mini",
    temperature=0.7
)

# Create the agent for generating solutions
agent = create_agent(
    llm,
    [think],  # You can add more tools if necessary
    TASK
)

def generate_solution(
    problem: str,
    customer_segments: str,
    existing_alternatives: str
) -> str:
    """
    Generate a solution based on the given problem, customer segments, and existing alternatives.

    Args:
        problem (str): The problem statement.
        customer_segments (str): A description of customer segments.
        existing_alternatives (str): A list of existing alternatives.

    Returns:
        str: A detailed description of the generated solution.
    """
    # Display a message in the Streamlit app
    st.markdown("## Generating a solution..")
    
    # Prepare the input for the agent
    input_data = {
        "problem": problem,
        "customer_segments": customer_segments,
        "existing_alternatives": existing_alternatives
    }
    
    # Invoke the agent with the problem, customer segments, and existing alternatives
    response = invoke_agent(agent, input_data)
    return response  # Return the generated solution as a string
