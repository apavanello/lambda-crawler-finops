import json
import os
from typing import List
from ..domain.models import InputItem

def load_input(file_path: str) -> List[InputItem]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    items = []
    for entry in data:
        if 'name' not in entry or 'account' not in entry:
            # Poderíamos logar um aviso e pular, ou falhar. 
            # Por hora, assumimos que o unit de validação pegaria isso, ou lançamos erro.
            raise ValueError(f"Invalid input format. Missing 'name' or 'account' in entry: {entry}")
            
        items.append(InputItem(
            name=entry['name'],
            account=str(entry['account']), # Garante string
            region=entry.get('region', 'us-east-1')
        ))
    return items

def save_errors(file_path: str, errors: List[dict]):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(errors, f, indent=2)
