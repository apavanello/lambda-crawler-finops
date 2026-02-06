import logging
import traceback
from typing import List
from crawler.domain.models import InputItem, LambdaResult
from crawler.services.aws import create_session, get_lambda_details, get_invocation_metrics, get_triggers
from crawler.services.profiles import load_aws_profiles

logger = logging.getLogger("LambdaCrawler")

def run_crawler(items: List[InputItem], days: int) -> List[LambdaResult]:
    """
    Main logic loop:
    1. Resolve Profile
    2. Connect AWS
    3. Fetch Data
    4. Compile Result
    """
    logger.info("Initializing Crawler Orchestrator...")
    
    # Pre-load profiles to avoid reading file 700 times
    profile_map = load_aws_profiles()
    results = []
    
    total = len(items)
    for idx, item in enumerate(items, 1):
        # Progress Log
        print(f"[{idx}/{total}] Processing {item.name} ({item.account})...")
        
        result = LambdaResult(
            function_name=item.name,
            account_id=item.account,
            region=item.region
        )
        
        try:
            # 1. Resolve Profile (MVP: Map Account -> Profile)
            profile_name = profile_map.get(item.account)
            
            # If not found, use default or try to find env vars? 
            # For MVP RNF: Must map SSO. If missing, Error.
            if not profile_name:
                raise ValueError(f"No profile found in ~/.aws/config for account {item.account}")
                
            # 2. Session
            session = create_session(profile_name, item.region)
            
            # 3. Fetch Details
            details = get_lambda_details(session, item.name)
            result.last_modified = details['LastModified']
            
            # 4. Fetch Metrics
            invocations, last_date = get_invocation_metrics(session, item.name, days)
            result.invocation_count_period = invocations
            result.last_invocation_date = last_date
            
            # 5. Fetch Triggers
            triggers = get_triggers(session, item.name)
            result.triggers_details = triggers
            result.trigger_count = len(triggers)
            result.has_triggers = len(triggers) > 0
            
            result.status = "SUCCESS"
            
        except Exception as e:
            # Log full trace to debug console, but clean message to report
            logger.error(f"Failed processing {item.name}: {e}")
            logger.debug(traceback.format_exc())
            result.status = "ERROR"
            result.error_message = str(e)
            result.error_type = type(e).__name__
            
        results.append(result)
        
    return results
