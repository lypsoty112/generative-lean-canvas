from langchain_openai import ChatOpenAI
from src.calls.tools.think import think
from src.calls.constants import CONTEXT, API_KEY
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

PROMPT =  """ 
You have access to the following tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think critically about what to do next and consider using the tools multiple times for a comprehensive exploration
Action: the action to take, should be one of [{tool_names}], e.g. 'think-tool' or 'search-tool'
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation cycle should repeat until you feel confident about your conclusions)

Thought: I now know the final answer
Final Answer: A bullet-point list of potential customer segments.

Provide the final answer as just a bullet-point list.

Begin!

input: {input}
Thought:{agent_scratchpad}
"""


def create_agent(
        llm, tools, task,
) -> AgentExecutor:
    prompt = PromptTemplate.from_template(task + "\n\n" + PROMPT)
    
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False, max_iterations=50, max_execution_time=120)


def invoke_agent(
        agent: AgentExecutor, input: any
) -> str:
    max_retries = 3  # Set the maximum number of retries
    for attempt in range(max_retries):
        try:
            # Invoke the agent executor with the problem input
            response = agent.invoke({
                "input": input
            })  
            
            # Check if the response has the expected output
            if response and 'output' in response:
                return response['output']
            else:
                # Print the thoughts to the console (you can customize this further)
                print(f"Attempt {attempt + 1}: No valid customer segments found.")
        
        except Exception as e:
            # Print the exception for debugging purposes
            print(f"Attempt {attempt + 1} failed: {str(e)}")
        
        # Optionally, you can add a brief sleep before retrying (uncomment the next line if needed)
        # time.sleep(1)  
    
    # If all attempts fail, raise an error
    raise RuntimeError("Failed to generate customer segments after 3 attempts.")
