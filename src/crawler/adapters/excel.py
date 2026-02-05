import pandas as pd
from typing import List, Dict
import logging
from ..domain.models import LambdaResult
from datetime import datetime

logger = logging.getLogger("LambdaCrawler")

def generate_report(results: List[LambdaResult], output_path: str = "report.xlsx"):
    """
    Generates a multi-sheet Excel report from the results.
    Separates by Account ID and creates an Exceptions sheet.
    """
    if not results:
        logger.warning("No results to write to Excel.")
        return
        
    logger.info(f"Generating Excel report at {output_path}...")
    
    # 1. Prepare Data
    success_data = [] # List of dicts
    error_data = []   # List of dicts
    
    for r in results:
        if r.status == "ERROR":
            error_data.append({
                "Function Name": r.function_name,
                "Account ID": r.account_id,
                "Region": r.region,
                "Error": r.error_message,
                "Type": r.error_type
            })
        else:
            lm_val = r.last_modified
            if lm_val and isinstance(lm_val, datetime):
                lm_val = lm_val.replace(tzinfo=None)
            
            success_data.append({
                "Function Name": r.function_name,
                "Account ID": r.account_id,
                "Region": r.region,
                "Last Modified": lm_val,
                "Invocations (Period)": r.invocation_count_period,
                "Has Triggers": r.has_triggers,
                "Trigger Count": r.trigger_count,
                "Triggers": ", ".join(r.triggers_details) if r.triggers_details else ""
            })
            
    # 2. Group by Account
    df_success = pd.DataFrame(success_data)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        if not df_success.empty:
            accounts = df_success['Account ID'].unique()
            for acc in accounts:
                df_acc = df_success[df_success['Account ID'] == acc]
                sheet_name = f"Acc_{acc}"[:31] # Excel limit 31 chars
                df_acc.to_excel(writer, sheet_name=sheet_name, index=False)
                logger.info(f"Added sheet {sheet_name} with {len(df_acc)} rows.")
        else:
            # Create a blank sheet so file is valid if only errors exist
            pd.DataFrame(["No successful audits"]).to_excel(writer, sheet_name="Summary", header=False)

        # 3. Exceptions Sheet
        if error_data:
            df_errors = pd.DataFrame(error_data)
            df_errors.to_excel(writer, sheet_name="Exceptions", index=False)
            logger.info(f"Added Exceptions sheet with {len(df_errors)} rows.")
            
    logger.info("Report generation complete.")
