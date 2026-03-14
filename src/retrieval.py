# src/retrieval.py

import pandas as pd

def get_schedule_context(similar_ids: list, schedule_df: pd.DataFrame) -> str:
    """
    Retrieves and formats schedule data for the given project IDs into a text context.
    """
    matched_schedules = schedule_df[schedule_df['MAIN_PROJECTID'].isin(similar_ids)]
    
    if matched_schedules.empty:
        return "No historical schedule data found for these projects."

    context_str = "HISTORICAL PROJECT SCHEDULES:\n"
    context_str += "="*40 + "\n\n"
    
    
    grouped = matched_schedules.groupby('MAIN_PROJECTID')
    
    for pid, group in grouped:
        context_str += f"--- Reference Project ID: {pid} ---\n"
        
        
        for _, row in group.iterrows():
            parent_task = row.get('PARWBSNAME', 'None')
            task = row.get('WBSNAME', 'Unknown Task')
            start = row.get('PLANNEDSTARTDATE', 'N/A')
            end = row.get('PLANNEDFINISHDATE', 'N/A')
            
            
            context_str += f"- Phase: {parent_task} | Task: {task} | Start: {start} | End: {end}\n"
        
        context_str += "\n" 
        
    return context_str