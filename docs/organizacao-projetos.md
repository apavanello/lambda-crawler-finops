# Organização do Projeto

## Estrutura de Diretórios
Seguiremos um layout padrão Python (src-layout) modernizado para uso com `uv`.

```text
lambda-crawler-finops/
├── .venv/                  # Virtual Environment (gerenciado pelo uv)
├── docs/                   # Documentação do projeto
├── src/
│   └── crawler/            # Código Fonte Principal
│       ├── __init__.py
│       ├── main.py         # Entrypoint CLI
│       ├── orchestrator.py # Lógica de Controle
│       ├── domain/
│       │   └── models.py   # Dataclasses
│       ├── services/
│       │   ├── aws.py      # Wrapper Boto3
│       │   └── profiles.py # Parser de Config
│       └── adapters/
│           ├── excel.py    # Gerador de Relatório
│           └── storage.py  # IO JSON
├── tests/                  # Testes Unitários
├── pyproject.toml          # Configuração UV e Dependências
├── Makefile                # Aliases de comandos (Build, Run, Clean)
└── README.md
```

## Ferramentas e Pipeline

### Gerenciamento de Pacotes (`uv`)
- **Dependências de Runtime:** `boto3`, `pandas`, `openpyxl`, `click`/`argparse`.
- **Dependências de Dev:** `pytest`, `ruff` (linter), `black` (formatter).

### Makefile
Automação simples para Windows (PowerShell) e Linux.
```makefile
setup:
	uv venv
	uv pip install -e .

run:
	uv run python src/crawler/main.py --input data/input.json --days 180

clean:
	# Comandos de limpeza
```

### Controle de Versão
- **Repositório Único (Monorepo):** Todo o código, docs e scripts em um só lugar.
- **Gitignore:** Ignorar `.venv`, `__pycache__`, `*.xlsx`, `*.csv`.
