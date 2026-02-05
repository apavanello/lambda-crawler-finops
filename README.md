# Lambda Crawler FinOps

Ferramenta CLI para auditoria de funções AWS Lambda em múltiplas contas. O objetivo é identificar funções ociosas ("Zumbis") analisando métricas de execução reais e configurações de gatilhos.

## Funcionalidades

- **Multi-Account via SSO:** Identifica automaticamente qual profile AWS usar com base no Account ID.
- **Métricas Reais:** Consulta o CloudWatch para saber quantas vezes a função rodou nos últimos X dias.
- **Auditoria de Triggers:** Verifica se a função possui gatilhos ativos (Event Source Mappings).
- **Relatório Excel:** Gera um arquivo `.xlsx` com abas separadas por conta.
- **Resiliência:** Em caso de falha em uma lambda, o sistema continua e gera um JSON de erros para retry.

## Pré-requisitos

- **Python 3.12+**
- **uv** (Gerenciador de pacotes)
- **AWS CLI v2** configurado com SSO (`aws configure sso`).
  - O arquivo `~/.aws/config` deve conter os profiles mapeados com `sso_account_id`.

## Instalação

1. Clone o repositório:
   ```bash
   git clone <repo-url>
   cd lambda-crawler-finops
   ```

2. Configure o ambiente usando `make`:
   ```powershell
   # Windows (PowerShell) / Linux
   make setup
   ```
   *Isso criará o ambiente virtual e instalará as dependências.*

## Como Usar

### 1. Prepare o Input
Crie um arquivo JSON (ex: `lambdas.json`) com as funções que deseja auditar:
```json
[
  {
    "name": "minha-funcao-prod",
    "account": "123456789012",
    "region": "us-east-1"
  },
  {
    "name": "outra-funcao-dev",
    "account": "987654321098"
  }
]
```

### 2. Execute o Crawler
Use o comando `make run` ou chame via `uv`:

```bash
# Execução padrão (Janela de 180 dias)
uv run python src/crawler/main.py --input lambdas.json

# Alterando a janela de tempo (ex: 90 dias)
uv run python src/crawler/main.py --input lambdas.json --days 90

# Modo de Teste (Limitar a 5 itens)
uv run python src/crawler/main.py --input lambdas.json --limit 5
```

## Resultados (Output)

Ao final da execução, dois arquivos serão gerados:

1.  **`lambda_audit_report.xlsx`**:
    -   **Abas de Conta:** Uma aba para cada Account ID processado. Contém dados de Última Modificação, Contagem de Invocações e Triggers.
    -   **Aba Exceptions:** Lista de erros (ex: AccessDenied, ResourceNotFound) para análise.

2.  **`errors.json`**:
    -   Arquivo no mesmo formato do input contendo apenas os itens que falharam. Pode ser usado diretamente como input para uma nova execução (Retry).

## Estrutura do Projeto

- `src/crawler`: Código fonte da aplicação.
- `docs/`: Documentação de arquitetura e planos.
- `data/`: Arquivos de exemplo.

## Solução de Problemas

**Erro: "No profile found for account..."**
Verifique se você fez login no AWS SSO (`aws sso login --profile <nome>`) e se o Account ID da lambda consta no seu `~/.aws/config`.

**Erro de Permissão (Access Denied)**
Garanta que o profile utilizado tem permissão de leitura (`lambda:GetFunction`, `cloudwatch:GetMetricStatistics`, `lambda:ListEventSourceMappings`).
