# Plano de Setup de Desenvolvimento

## Configuração do Repositório e Ambiente
- [ ] Inicializar Git Repository e criar `.gitignore` (Python)
- [ ] Instalar `uv` (caso não tenha)
- [ ] Executar `uv init` para criar `pyproject.toml`
- [ ] Criar arquivo `Makefile` com comandos (`setup`, `run`, `clean`)
- [ ] Configurar `.python-version` para garantir compatibilidade (3.12+)

## Dependências e Ferramentas
- [ ] Adicionar dependências de Runtime via `uv add`:
  - `boto3`
  - `click` (ou `argparse` nativo, conforme decisão de arquitetura components.md usou argparse/click) -> Vou usar `click` pela facilidade.
  - `pandas`
  - `openpyxl`
- [ ] Adicionar dependências de Dev via `uv add --dev`:
  - `pytest`
  - `ruff` (linter/formatter)
  - `black` (opcional, ruff já cobre)

## Estrutura de Pastas
- [ ] Criar estrutura `src/crawler`
- [ ] Criar subpastas: `domain`, `services`, `adapters`
- [ ] Criar pasta `tests`
- [ ] Criar pasta `data` (para inputs de teste)
