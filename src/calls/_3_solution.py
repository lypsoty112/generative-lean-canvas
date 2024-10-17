from langchain_openai import ChatOpenAI
import streamlit as st
from src.calls.constants import API_KEY, CONTEXT
from langchain_core.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from operator import itemgetter
from langchain.globals import set_debug

set_debug(True)

# Define the task for generating a solution

TASK1 = CONTEXT + """
Problem: {problem}
Customer segments:
```
{customer_segments}
```

Existing alternatives:
```
{existing_alternatives}
```

Write down your thoughts on how you would create a business that solves the problem for the customer segments, & is different from the alternatives.

"""

TASK2 = CONTEXT + """ 

Problem: {problem}
Customer segments:
```
{customer_segments}
```
Thoughts: 
```
{thoughts}
```



Generate a comprehensive description based of the business that's thought about. The business will solve the given problem for the given customer segments.
Your description should be about 4 short sentences.
"""


# Initialize the language model
llm1 = ChatOpenAI(
    api_key=API_KEY,
    temperature=1,
    model="gpt-4o-mini",
    max_retries=0,
)

llm2 = ChatOpenAI(
    api_key=API_KEY,
    temperature=0.7,
    model="gpt-4o-mini",
    max_retries=0,
)


# Create a prompt template from the task
prompt1 = PromptTemplate.from_template(TASK1)
prompt2 = PromptTemplate.from_template(TASK2)


# Create a chain that includes the prompt and language model

chain1 = prompt1 | llm1 | StrOutputParser()

chain = ({
    "problem": itemgetter("problem"),
    "customer_segments": itemgetter("customer_segments"),
    "thoughts": chain1
} | prompt2 | llm2 | StrOutputParser())

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

    # Prepare the input for the chain
    input_data = {
        "problem": problem,
        "customer_segments": customer_segments,
        "existing_alternatives": existing_alternatives
    }
    
    # Invoke the chain with the input data
    response = chain.invoke(input_data)
    return response  # Return the generated solution as a string
