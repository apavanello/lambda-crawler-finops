# Documento de Intenção: Lambda Crawler FinOps

## Resumo Executivo
Desenvolvimento de uma ferramenta CLI (MVP) para automação de auditoria FinOps em funções AWS Lambda. O objetivo é varrer uma lista específica de funções em múltiplas contas AWS e extrair métricas reais de utilização e configuração para identificar recursos ociosos ou abandonados.

## Problema a Resolver
Dificuldade em auditar em massa o estado real de funções Lambda distribuídas em várias contas. Apenas saber a "Data de Modificação" é insuficiente; é necessário cruzar com dados de execução (invocação) e configuração de gatilhos para determinar se o recurso ainda é necessário.

## Público-Alvo
- Engenheiros de FinOps
- Cloud Engineers / SREs
- Gerentes de Custos Cloud

## Visão da Solução (MVP)

### Fluxo de Trabalho
1. **Entrada:** O usuário fornece um arquivo **JSON** contendo uma lista de Lambdas e suas respectivas contas AWS.
2. **Descoberta de Credenciais:** O sistema lê o arquivo local `~/.aws/config` para encontrar qual profile SSO corresponde ao Account ID fornecido.
3. **Coleta de Dados:**
    - Conecta na conta AWS correta.
    - Busca metadados da função (`LastModified`).
    - Consulta CloudWatch Metrics para buscar invocações nos últimos **6 meses** (Última Execução Real).
    - Lista e conta todos os gatilhos (Event Sources) ativos.
4. **Saída:** Gera uma planilha **Excel** consolidada, separando os dados de cada conta em uma aba (sheet) diferente.

## Detalhes Técnicos Chave
- **Linguagem:** Python
- **Gerenciador de Pacotes:** `uv` (substituto moderno para pip/poetry) + Makefile para setup.
- **Definição de "Uso":** Combinação de `LastModified` (deploy) e Metrics Invocations (uso real).

## Matriz de Decisões
- **Input:** JSON (Campos: `name`, `account`).
- **Profiles:** Parse manual de `~/.aws/config` para mapear `account_id` -> `profile_name`.
- **Janela de Busca:** 6 meses de histórico no CloudWatch.
- **Trigger:** Contabilizar qualquer fonte de evento configurada.
