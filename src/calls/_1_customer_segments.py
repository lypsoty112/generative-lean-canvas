
from langchain_openai import ChatOpenAI
import streamlit as st
from src.calls.main import create_agent, invoke_agent
from src.calls.tools.think import think
from src.calls.constants import API_KEY

TASK = "Think long and hard about the given problem's possible customer segments. In your final answer, provide a bullet-point list of customer segments."

tools = [
    think
]
 
llm = ChatOpenAI(
    api_key=API_KEY,
    model="gpt-4o-mini",
    temperature=0.7
)

agent = create_agent(
    llm,
    tools,
    TASK
)


def generate_customer_segments(
        problem: str
) -> str:
    st.markdown("## Thinking about customer segments..")
    response = invoke_agent(agent, {
        "problem": problem
    })
    return response
