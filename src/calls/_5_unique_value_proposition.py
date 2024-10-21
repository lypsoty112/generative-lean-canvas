from langchain_openai import ChatOpenAI
from src.calls.constants import API_KEY, CONTEXT
from langchain_core.prompts import PromptTemplate
from langchain.schema import StrOutputParser

PROMPT = CONTEXT + """

Problem: {problem}
Customer segments:
```
{customer_segments}
```

Provided business/solution:
```
{solution}
```

Existing Alternatives:
```
{alternatives}
```

Write down this business' unique value proposition in exactly 1 sentence of 10 words. Only write down the value proposition.

Unique value proposition:
"""

chain = None
def build():
    global chain
    llm1 = ChatOpenAI(
        api_key=API_KEY,
        temperature=0.75,
        model="gpt-4o-mini",
        max_retries=0,
    )

    prompt = PromptTemplate.from_template(PROMPT)


    chain = prompt | llm1 | StrOutputParser()


def generate_unique_value_proposition(
    problem: str,
    customer_segments: str,
    existing_alternatives: str,
    solution: str,
    high_level_concept:str
):
    input_data = {
        "problem": problem,
        "customer_segments": customer_segments,
        "alternatives": existing_alternatives,
        "solution": solution
    }
    
    response = chain.invoke(input_data)
    return response

    # TODO: Generate  a list