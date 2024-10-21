from langchain.tools import tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from src.calls.constants import API_KEY

class ThinkInput(BaseModel):
    task: str = Field(description="Should be a very descriptive task of what to think about. Includes context, task & current state")



PROMPT = """
You're a very smart thinker that has to think about things. 
Right now, think about this & provide a logical, well-thought out response:
```
{task}
```


Response:
"""

chain = None
def build():
    global chain
    prompt = PromptTemplate.from_template(PROMPT)

    llm = ChatOpenAI(
        api_key=API_KEY,
        model="gpt-4o-mini",
        temperature=0.3
    )


    chain = prompt | llm



@tool("think-tool", args_schema=ThinkInput)
def think(task: str):
    """Think about something & provide a well-thought out answer.
    INPUT: Should be a very descriptive task of what to think about. Includes context, task & current state
    
    """
    response: AIMessage = chain.invoke({
        "task": task
    })

    return response.content

