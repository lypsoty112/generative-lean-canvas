import streamlit as st

# Import all the required functions from their respective files
from src.calls._1_customer_segments import generate_customer_segments
from src.calls._2_existing_alternatives import generate_existing_alternatives
from src.calls._3_solution import generate_solution
from src.calls._4_high_level_concept import generate_high_level_concept
from src.calls._5_unique_value_proposition import generate_unique_value_proposition
from src.calls._6_channels import generate_channels
from src.calls._7_revenue_streams import generate_revenue_streams
from src.calls._8_cost_structure import generate_cost_structure
from calls._9_early_adopters import generate_early_adopters
from src.calls._10_key_metrics import generate_key_metrics
from src.calls._11_unfair_advantage import generate_unfair_advantage


def generate(
    problem: str,
    existing_alternatives: str = "",
    customer_segments: str = "",
    early_adopters: str = "",
    unique_value_proposition: str = "",
    high_level_concept: str = "",
    solution: str = "",
    channels: str = "",
    revenue_streams: str = "",
    cost_structure: str = "",
    key_metrics: str = "",
    unfair_advantage: str = "",
) -> dict[str, str]:
    """
    1. Problem
    2. Customer segments
    3. Existing alternatives
    4. Solution
    5. High level concept
    6. Unique value proposition 
    7. Channels
    8. Revenue streams
    9. Cost structure
    10. Early adopters
    11. Key metrics
    12. Unfair advantage
    """
    # Ensure that 'problem' is not empty
    if not problem:
        raise ValueError("The 'Problem' field is required.")

    st.markdown("# Generating...")

    # Call each method sequentially
    customer_segments = generate_customer_segments(problem)
    existing_alternatives = generate_existing_alternatives(problem, customer_segments)
    solution = generate_solution(problem, customer_segments, existing_alternatives)
    high_level_concept = generate_high_level_concept(problem, customer_segments, existing_alternatives, solution)
    unique_value_proposition = generate_unique_value_proposition(problem, customer_segments, existing_alternatives, solution, high_level_concept)
    channels = generate_channels(problem, customer_segments, existing_alternatives, solution, high_level_concept, unique_value_proposition)
    revenue_streams = generate_revenue_streams(problem, customer_segments, existing_alternatives, solution, high_level_concept, unique_value_proposition, channels)
    cost_structure = generate_cost_structure(problem, customer_segments, existing_alternatives, solution, high_level_concept, unique_value_proposition, channels, revenue_streams)
    early_adopters = generate_early_adopters(problem, customer_segments, existing_alternatives, solution, high_level_concept, unique_value_proposition, channels, revenue_streams, cost_structure)
    key_metrics = generate_key_metrics(problem, customer_segments, existing_alternatives, solution, high_level_concept, unique_value_proposition, channels, revenue_streams, cost_structure, early_adopters)
    unfair_advantage = generate_unfair_advantage(problem, customer_segments, existing_alternatives, solution, high_level_concept, unique_value_proposition, channels, revenue_streams, cost_structure, early_adopters, key_metrics)

    # Return the results as a dictionary
    return {
        "problem": problem,
        "customer_segments": customer_segments,
        "existing_alternatives": existing_alternatives,
        "solution": solution,
        "high_level_concept": high_level_concept,
        "unique_value_proposition": unique_value_proposition,
        "channels": channels,
        "revenue_streams": revenue_streams,
        "cost_structure": cost_structure,
        "early_adopters": early_adopters,
        "key_metrics": key_metrics,
        "unfair_advantage": unfair_advantage,
    }
