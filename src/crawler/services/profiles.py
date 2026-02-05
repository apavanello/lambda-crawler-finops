import os
import re
from typing import Dict

def load_aws_profiles() -> Dict[str, str]:
    """
    Parses ~/.aws/config to map Account IDs to Profile Names.
    Returns a dict: { '123456789012': 'my-sso-profile-name', ... }
    """
    config_path = os.path.expanduser("~/.aws/config")
    mapping = {}
    
    if not os.path.exists(config_path):
        # Fallback silencioso ou warning? Para MVP, retorna vazio e logaremos erro depois se não achar.
        return mapping

    current_profile = None
    
    # Regex simples para capturar cabeçalho [profile nome] e [nome]
    # E buscar sso_account_id = ...
    # Nota: AWS CLI config pode ter formatos variados. Focaremos no padrão SSO.
    
    profile_pattern = re.compile(r"^\[(?:profile\s+)?(.+)\]")
    account_pattern = re.compile(r"^sso_account_id\s*=\s*(\d+)")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            prof_match = profile_pattern.match(line)
            if prof_match:
                current_profile = prof_match.group(1)
                continue
                
            if current_profile:
                acc_match = account_pattern.match(line)
                if acc_match:
                    account_id = acc_match.group(1)
                    mapping[account_id] = current_profile
                    
    return mapping
