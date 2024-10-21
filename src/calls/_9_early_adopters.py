# 10. Early Adopters
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
Write down a detailed description of 1 or more customer segments who would most likely be the early adopters of this product/service. Include characteristics, behaviors, and needs. Start with "Early adopters include: ..."

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

Proposed Early Adopters:
``
{early_adopters}
``

Reasoning:
``
{reasoning}
``

---
# TASK
Take the provided early adopters segment(s) and reason through the logic. Attempt to refine or add detail to the early adopters' characteristics, behaviors, and needs. Provide a paragraph to describe the customers. Start with "Early adopters include: ..."
Provide your final answer as a short answer of about 2 sentences. Use Markdown formatting.


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
        ResponseSchema(name="Early adopters", description="The proposed early adopters' segment(s) with detailed description.")
    ])

    output_parser2 = StructuredOutputParser.from_response_schemas([
        ResponseSchema(name="Reasoning and thoughts", description="Write down your thoughts & reasoning here before answering."),
        ResponseSchema(name="Cannot be further optimized", description="'No' if you plan on proposing changes to the early adopters, 'Yes' if the early adopters segment(s) cannot be further optimized."),
        ResponseSchema(name="Optimized early adopters", description="The new and optimized early adopters' segment(s) with additional detail."),
    ])

    prompt1 = PromptTemplate.from_template(PROMPT1, partial_variables={"format_instructions": output_parser1.get_format_instructions()})
    prompt2 = PromptTemplate.from_template(PROMPT2, partial_variables={"format_instructions": output_parser2.get_format_instructions()})

    init_chain = prompt1 | llm1 | output_parser1
    secondary_chain = prompt2 | llm2 | output_parser2


def generate_early_adopters(problem: str, customer_segments: str, existing_alternatives: str, solution: str, high_level_concept: str, unique_value_proposition: str, channels: str) -> str:
    
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
        "early_adopters": response.get("Early adopters")
    }
    
    counter = 0
    stop = False
    while counter < 3 and not stop:  # Only loop three times
        response = secondary_chain.invoke(input_data)
        # Update the input data again
        input_data = {
            **input_data,
            "reasoning": response.get("Reasoning and thoughts", None),
            "early_adopters": response.get("Optimized early adopters"),
        }

        stop = response.get("Cannot be further optimized", "no").lower() == "no"

        counter += 1

    return input_data["early_adopters"]
