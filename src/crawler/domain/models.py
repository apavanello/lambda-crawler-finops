from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class InputItem:
    name: str
    account: str
    region: Optional[str] = None

@dataclass
class LambdaResult:
    function_name: str
    account_id: str
    region: str
    
    # Metadata
    last_modified: Optional[datetime] = None
    
    # Metrics
    last_invocation_date: Optional[datetime] = None # Derivado ou aproximado
    invocation_count_period: int = 0
    
    # Triggers
    has_triggers: bool = False
    trigger_count: int = 0
    triggers_details: List[str] = field(default_factory=list)
    
    # Status/Audit
    status: str = "PENDING" # SUCCESS, ERROR, SKIPPED
    error_message: Optional[str] = None
    error_type: Optional[str] = None
