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

Examples:
- `The Spotify of printing`
- `Like Tinder, but for biking`
- `Uber combined with Hotels`
- ...

Provide a short, high-level concept describing the business idea. I've provided some examples.
Only provide the high-level concept. 


high-level concept:
"""

chain = None

def build():
    global chain
    llm1 = ChatOpenAI(
        api_key=API_KEY,
        temperature=0.1,
        model="gpt-4o-mini",
        max_retries=0,
    )

    prompt = PromptTemplate.from_template(PROMPT)


    chain = prompt | llm1 | StrOutputParser()

def generate_high_level_concept(
    problem: str,
    customer_segments: str,
    existing_alternatives: str,
    solution: str
):
    input_data = {
        "problem": problem,
        "customer_segments": customer_segments,
        "solution": solution
    }
    
    response = chain.invoke(input_data)
    return response