# src/llm_agent.py

import os
from openai import AzureOpenAI

def generate_schedule(new_project_details: dict, historical_context: str) -> str:
    """Initial Generation Function."""
    client = AzureOpenAI(
        azure_endpoint="https://vcon.openai.azure.com/",
        api_key=os.getenv("AZURE_OPENAI_KEY"), 
        api_version="2024-12-01-preview"
    )
    
    system_prompt = """
    You are an expert Construction Planner. 
    Output structure:
    # Recommended Project Schedule
    [Markdown Table]
    
    ## Summary
    [Brief project overview]
    
    <CSV_START>
    Task,Phase,Start_Day,Duration,Cost,Critical,Labor
    ...
    <CSV_END>
    
    CRITICAL: Stop all text immediately after the Summary. 
    The CSV block must be the very last thing.
    """
    
    user_prompt = f"PROJECT: {new_project_details}\n\nDATA: {historical_context}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.2,
            max_tokens=2500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def refine_schedule(current_schedule: str, user_instruction: str) -> str:
    """Refinement and Simulation function."""
    client = AzureOpenAI(
        azure_endpoint="https://vcon.openai.azure.com/",
        api_key=os.getenv("AZURE_OPENAI_KEY"), 
        api_version="2024-12-01-preview"
    )

    system_prompt = """
    You are a Scheduling Assistant. Update the project schedule.
    Return:
    - Brief explanation.
    - Full updated Markdown Table.
    
    Then start the hidden data block:
    <CSV_START>
    Task,Phase,Start_Day,Duration,Cost,Critical,Labor
    ...
    <CSV_END>
    
    STRICT: Ensure the Markdown table is fully rendered before the <CSV_START> tag.
    """

    user_prompt = f"CURRENT: {current_schedule}\n\nREQUEST: {user_instruction}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.1,
            max_tokens=2500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"