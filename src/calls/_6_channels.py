from operator import itemgetter
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from src.calls.constants import API_KEY, CONTEXT
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

PROMPT1 = CONTEXT + """
problem: "{problem}"
Customer segments:
```
{customer_segments}
```

Provided business/solution:
```
{solution}
```

Unique value proposition:
```
{unique_value_proposition}
```

Existing Alternatives:
```
{alternatives}
```


Write down this business' optimal channel strategy in exactly 1 paragraph.

{format_instructions}
"""

PROMPT2 = CONTEXT + """
Problem: "{problem}"
Customer segments:
```
{customer_segments}
```

Provided business/solution:
```
{solution}
```

Unique value proposition:
```
{unique_value_proposition}
```

Existing Alternatives:
```
{alternatives}
```

----
Proposed channel strategy:
```
{channels}
```
Reasoning: 
```
{reasoning}
```

Take the provided channel strategy for this business & reason through the logic & attempt to come to a more logical or reasonable conclusion.
Provide your final answer as a short answer of about 2 sentences. Use Markdown formatting

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
        ResponseSchema(name="Channel strategy", description="The proposed channel strategy")
    ])

    output_parser2 = StructuredOutputParser.from_response_schemas([
        ResponseSchema(name="Reasoning and thoughts", description="Write down your thoughts & reasoning here before answering."),
        ResponseSchema(name="Cannot be further optimized", description="'No' if you plan on proposing changes to the strategy, 'Yes' if the strategy cannot be further optimized."),
        ResponseSchema(name="Optimized channel strategy", description="The new and optimized channel strategy"),
        
    ])

    prompt1 = PromptTemplate.from_template(PROMPT1, partial_variables={"format_instructions": output_parser1.get_format_instructions()})
    prompt2 = PromptTemplate.from_template(PROMPT2, partial_variables={"format_instructions": output_parser2.get_format_instructions()})


    init_chain = prompt1 | llm1 | output_parser1
    secondary_chain = prompt2 | llm2 | output_parser2


def generate_channels(problem: str, customer_segments: str, existing_alternatives: str, solution: str, high_level_concept: str, unique_value_proposition: str) -> str:
    """
    Generate an optimal channel strategy for the given business.

    Args:
        problem (str): The problem statement.
        customer_segments (str): Customer segments.
        existing_alternatives (str): Existing alternatives.
        solution (str): Provided business/solution.
        high_level_concept (str): High-level concept.
        unique_value_proposition (str): Unique value proposition.

    Returns:
        str: Optimal channel strategy.
    """
    
    input_data = {
        "problem": problem,
        "customer_segments": customer_segments,
        "alternatives": existing_alternatives,
        "solution": solution,
        "unique_value_proposition": unique_value_proposition
    }

    response = init_chain.invoke(input_data)

    input_data = {
        **input_data,
        "reasoning": response.get("Reasoning and thoughts", None),
        "channels": response.get("Channel strategy")
    }
    counter = 0
    stop = False
    while counter < 5 and not stop:
        response = secondary_chain.invoke(input_data)
        # Update the input data again
        input_data = {
            **input_data,
            "reasoning": response.get("Reasoning and thoughts", None),
            "channels": response.get("Optimized channel strategy"),
        }

        stop = response.get("Cannot be further optimized", "no").lower() == "no"

        counter += 1

    return input_data["channels"]