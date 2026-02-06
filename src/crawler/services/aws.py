import boto3
import json
import logging
from typing import Optional
from botocore.exceptions import ClientError, ProfileNotFound

logger = logging.getLogger("LambdaCrawler")

def create_session(profile_name: Optional[str], region: Optional[str] = None) -> boto3.Session:
    """
    Creates a Boto3 Session using the specified profile.
    If profile is None, uses default chain.
    If region is None, uses profile's configured region.
    """
    try:
        if profile_name:
            return boto3.Session(profile_name=profile_name, region_name=region)
        else:
            return boto3.Session(region_name=region)
    except ProfileNotFound:
        logger.error(f"Profile '{profile_name}' not found locally.")
        raise
    except Exception as e:
        logger.error(f"Failed to create AWS Session: {e}")
        raise

from datetime import datetime, timedelta
from dateutil.parser import parse

def get_parameters_client(session: boto3.Session):
    return session.client('ssm')

def get_cloudwatch_client(session: boto3.Session):
    return session.client('cloudwatch')

def get_lambda_client(session: boto3.Session):
    return session.client('lambda')

def get_lambda_details(session: boto3.Session, function_name: str) -> dict:
    """
    Fetches basic configuration including LastModified.
    """
    client = get_lambda_client(session)
    response = client.get_function(FunctionName=function_name)
    conf = response['Configuration']
    
    lm = conf.get('LastModified')
    if isinstance(lm, str):
        try:
            lm = parse(lm)
        except:
            pass # Keep as string or None if parse fails, though unlikely

    return {
        'LastModified': lm,
        'FunctionAm': conf.get('FunctionArn'),
        'Runtime': conf.get('Runtime'),
        'MemorySize': conf.get('MemorySize')
    }

from typing import Tuple, Optional

def get_invocation_metrics(session: boto3.Session, function_name: str, days: int) -> Tuple[int, Optional[datetime]]:
    """
    Queries CloudWatch for Sum of Invocations.
    Returns (Total Count, Last Execution Date).
    """
    client = get_cloudwatch_client(session)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)
    
    # 1. Get Total Count (Efficient single query)
    response = client.get_metric_statistics(
        Namespace='AWS/Lambda',
        MetricName='Invocations',
        Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400 * days, 
        Statistics=['Sum']
    )
    
    total_invocations = 0
    if 'Datapoints' in response:
        for dp in response['Datapoints']:
            total_invocations += int(dp.get('Sum', 0))
            
    last_date = None
    
    # 2. If active, find the last date (Granular query)
    if total_invocations > 0:
        # Query daily points
        daily_res = client.get_metric_statistics(
            Namespace='AWS/Lambda',
            MetricName='Invocations',
            Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
            StartTime=start_time,
            EndTime=end_time,
            Period=86400, # Daily granularity
            Statistics=['Sum']
        )
        
        # Sort by timestamp descending
        if 'Datapoints' in daily_res:
             sorted_dps = sorted(daily_res['Datapoints'], key=lambda x: x['Timestamp'], reverse=True)
             for dp in sorted_dps:
                 if dp.get('Sum', 0) > 0:
                     last_date = dp['Timestamp']
                     break
            
    return total_invocations, last_date

def get_triggers(session: boto3.Session, function_name: str) -> list:
    """
    Lists Event Source Mappings.
    Note: accessible via ListEventSourceMappings (Dynamo, Kinesis, SQS).
    Other triggers (API Gateway, EventBridge) are separate APIs. 
    For MVP user asked for "any type", but Lambda API mostly shows ESM.
    We will stick to ESM for now as described in docs, plus potentially Policy check if time permits.
    """
    client = get_lambda_client(session)
    triggers = []
    
    # 1. Event Source Mappings
    paginator = client.get_paginator('list_event_source_mappings')
    for page in paginator.paginate(FunctionName=function_name):
        for mapping in page['EventSourceMappings']:
            state = mapping.get('State')
            src = mapping.get('EventSourceArn')
            triggers.append(f"ESM: {src} ({state})")
            
    # 2. Function Policy (for permissions like S3, API Gateway, EventBridge)
    # This requires 'get_policy'. 
    try:
        policy_res = client.get_policy(FunctionName=function_name)
        policy = json.loads(policy_res['Policy'])
        for stmt in policy.get('Statement', []):
            principal = stmt.get('Principal', {})
            # Simplified trigger info
            svc = principal.get('Service', str(principal))
            triggers.append(f"Policy: {svc}")
    except client.exceptions.ResourceNotFoundException:
        pass # No policy means no external triggers of that type
    except Exception as e:
        logger.warning(f"Could not read policy for {function_name}: {e}")
        
    return triggers
