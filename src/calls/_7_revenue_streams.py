# 8. Revenue Streams
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from src.calls.constants import API_KEY, CONTEXT
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

PROMPT1 = CONTEXT + """
problem: "{problem}"
Customer segments:
``
{customer_segments}
``

Provided business/solution:
``
{solution}
``

Unique value proposition:
``
{unique_value_proposition}
``

Existing Alternatives:
``
{alternatives}
``

Channels:
``
{channels}
``
---
# TASK
Write down this revenue streams in exactly 1 paragraph. Start with "Revenue streams include: ..."

{format_instructions}
"""

PROMPT2 = CONTEXT + """
Problem: "{problem}"
Customer segments:
``
{customer_segments}
``

Provided business/solution:
``
{solution}
``

Unique value proposition:
``
{unique_value_proposition}
``

Existing Alternatives:
``
{alternatives}
``

Channels:
``
{channels}
``

----
Proposed Revenue streams:
``
{revenue_streams}
``
Reasoning: 
``
{reasoning}
``²

---
# TASK
Take the provided revenue streams for this business & reason through the logic & attempt to come to a more logical or reasonable conclusion.

{format_instructions}
"""

init_chain = None
secondary_chain = None
def build():
    global init_chain, secondary_chain

    llm1 = ChatOpenAI(
        api_key=API_KEY,
        temperature=0.75,
        model="gpt-4o-mini",
        max_retries=0,
    )

    llm2 = ChatOpenAI(
        api_key=API_KEY,
        temperature=0.75,
        model="gpt-4o-mini",
        max_retries=0,
    )

    output_parser1 = StructuredOutputParser.from_response_schemas([
        ResponseSchema(name="Reasoning and thoughts", description="Write down your thoughts & reasoning here before answering."),
        ResponseSchema(name="Revenue streams", description="The proposed revenue streams")
    ])

    output_parser2 = StructuredOutputParser.from_response_schemas([
        ResponseSchema(name="Reasoning and thoughts", description="Write down your thoughts & reasoning here before answering."),
        ResponseSchema(name="Cannot be further optimized", description="'No' if you plan on proposing changes to the revenue streams, 'Yes' if the revenue sreams cannot be further optimized."),
        ResponseSchema(name="Optimized revenue streams", description="The new and optimized revenue streams"),
        
    ])

    prompt1 = PromptTemplate.from_template(PROMPT1, partial_variables={"format_instructions": output_parser1.get_format_instructions()})
    prompt2 = PromptTemplate.from_template(PROMPT2, partial_variables={"format_instructions": output_parser2.get_format_instructions()})


    init_chain = prompt1 | llm1 | output_parser1
    secondary_chain = prompt2 | llm2 | output_parser2



def generate_revenue_streams(problem: str, customer_segments: str, existing_alternatives: str, solution: str, high_level_concept: str, unique_value_proposition: str, channels: str) -> str:
        
    input_data = {
        "problem": problem,
        "customer_segments": customer_segments,
        "alternatives": existing_alternatives,
        "solution": solution,
        "unique_value_proposition": unique_value_proposition,
        "channels": channels,
    }

    response = init_chain.invoke(input_data)

    input_data = {
        **input_data,
        "reasoning": response.get("Reasoning and thoughts", None),
        "revenue_streams": response.get("Revenue streams")
    }
    counter = 0
    stop = False
    while counter < 5 and not stop:
        response = secondary_chain.invoke(input_data)
        # Update the input data again
        input_data = {
            **input_data,
            "reasoning": response.get("Reasoning and thoughts", None),
            "revenue_streams": response.get("Optimized revenue streams"),
        }

        stop = response.get("Cannot be further optimized", "no").lower() == "no"

        counter += 1

    return input_data["revenue_streams"]