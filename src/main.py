import streamlit as st

# Import all the required functions from their respective files
from src.calls._1_customer_segments import generate_customer_segments, build as build_1
from src.calls._2_existing_alternatives import generate_existing_alternatives, build as build_2
from src.calls._3_solution import generate_solution, build as build_3
from src.calls._4_high_level_concept import generate_high_level_concept, build as build_4
from src.calls._5_unique_value_proposition import generate_unique_value_proposition, build as build_5
from src.calls._6_channels import generate_channels, build as build_6
from src.calls._7_revenue_streams import generate_revenue_streams, build as build_7
from src.calls._8_cost_structure import generate_cost_structure, build as build_8
from src.calls._9_early_adopters import generate_early_adopters, build as build_9
from src.calls._10_key_metrics import generate_key_metrics, build as build_10
from src.calls._11_unfair_advantage import generate_unfair_advantage, build as build_11
from src.calls.tools.think import build as build_think
from src.calls.constants import set_api_key
import concurrent.futures
from typing import Callable

def execute_build(build_func: Callable):
    build_func()

def build(api_key: str | None):
    set_api_key(api_key)
    
    build_functions = [
        build_1, build_2, build_3, build_4, build_5,
        build_6, build_7, build_8, build_9, build_10, build_11, build_think
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(execute_build, func) for func in build_functions]
        concurrent.futures.wait(futures)

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

    # Step 1: Customer Segments
    st.markdown("## Step 1: Customer Segments")
    if not customer_segments:
        customer_segments = generate_customer_segments(problem)
    st.markdown(f"{customer_segments}")

    # Step 2: Existing Alternatives
    st.markdown("## Step 2: Existing Alternatives")
    if not existing_alternatives:
        existing_alternatives = generate_existing_alternatives(problem, customer_segments)
    st.markdown(f"{existing_alternatives}")

    # Step 3: Solution
    st.markdown("## Step 3: Solution")
    if not solution:
        solution = generate_solution(problem, customer_segments, existing_alternatives)
    st.markdown(f"{solution}")

    # Step 4: High-Level Concept
    st.markdown("## Step 4: High-Level Concept")
    if not high_level_concept:
        high_level_concept = generate_high_level_concept(problem, customer_segments, existing_alternatives, solution)
    st.markdown(f"{high_level_concept}")

    # Step 5: Unique Value Proposition
    st.markdown("## Step 5: Unique Value Proposition")
    if not unique_value_proposition:
        unique_value_proposition = generate_unique_value_proposition(problem, customer_segments, existing_alternatives, solution, high_level_concept)
    st.markdown(f"{unique_value_proposition}")

    # Step 6: Channels
    st.markdown("## Step 6: Channels")
    if not channels:
        channels = generate_channels(problem, customer_segments, existing_alternatives, solution, high_level_concept, unique_value_proposition)
    st.markdown(f"{channels}")

    # Step 7: Revenue Streams
    st.markdown("## Step 7: Revenue Streams")
    if not revenue_streams:
        revenue_streams = generate_revenue_streams(problem, customer_segments, existing_alternatives, solution, high_level_concept, unique_value_proposition, channels)
    st.markdown(f"{revenue_streams}")

    # Step 8: Cost Structure
    st.markdown("## Step 8: Cost Structure")
    if not cost_structure:
        cost_structure = generate_cost_structure(problem, customer_segments, existing_alternatives, solution, high_level_concept, unique_value_proposition, channels, revenue_streams)
    st.markdown(f"{cost_structure}")

    # Step 9: Early Adopters
    st.markdown("## Step 9: Early Adopters")
    if not early_adopters:
        early_adopters = generate_early_adopters(problem, customer_segments, existing_alternatives, solution, high_level_concept, unique_value_proposition, channels)
    st.markdown(f"{early_adopters}")

    # Step 10: Key Metrics
    st.markdown("## Step 10: Key Metrics")
    if not key_metrics:
        key_metrics = generate_key_metrics(problem, customer_segments, existing_alternatives, solution, high_level_concept, unique_value_proposition, channels, revenue_streams, cost_structure, early_adopters)
    st.markdown(f"{key_metrics}")

    # Step 11: Unfair Advantage
    st.markdown("## Step 11: Unfair Advantage")
    if not unfair_advantage:
        unfair_advantage = generate_unfair_advantage(problem, customer_segments, existing_alternatives, solution, high_level_concept, unique_value_proposition, channels, revenue_streams, cost_structure, early_adopters, key_metrics)
    st.markdown(f"{unfair_advantage}")

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
