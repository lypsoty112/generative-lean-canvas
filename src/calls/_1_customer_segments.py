
from langchain_openai import ChatOpenAI
import streamlit as st
from src.calls.constants import API_KEY, CONTEXT
from langchain_core.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from operator import itemgetter


TASK1 = CONTEXT + """

Problem: {problem}

Generate a numbered list of about 80 possible customer segments for the given problem. Make sure to range from very broad to very specific.
Provide only the list as a numbered list:
"""


TASK2 = CONTEXT + """

Problem: {problem}
Customer segments:
```
{segments}
```

Of these segments, select the 5 most logical customer segments for the provided problem. You're also allowed to add other segments if you see fit.
Provide only the list as a numbered list:
"""

chain = None

def build():
    global chain
    llm1 = ChatOpenAI(
        api_key=API_KEY,
        temperature=1,
        model="gpt-4o-mini",
        max_retries=0,


    )
    llm2 = ChatOpenAI(
        api_key=API_KEY,
        temperature=.4,
        model="gpt-4o-mini",
        
    )

    prompt1 = PromptTemplate.from_template(
        TASK1,
    )
    prompt2 = PromptTemplate.from_template(
        TASK2,
    )

    chain1 = prompt1 | llm1 | StrOutputParser()

    chain = ({
        "segments": chain1,
        "problem": itemgetter("problem")
    } | prompt2 | llm2| StrOutputParser())



def generate_customer_segments(
        problem: str
) -> str:
    response = chain.invoke({
        "problem": problem,
    })
    return response
