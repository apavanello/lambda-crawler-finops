# Priorização e Classificação de Features

| ID | Feature | Classificação (MoSCoW) | Esforço Estimado | Skills Necessárias |
|:---|:---|:---|:---|:---|
| 1 | **Leitura e Validação de Input** | MUST HAVE | Baixo | Python (IO, JSON) |
| 2 | **Descoberta Automática de Profiles SSO** | MUST HAVE | Médio | Python (Regex/Parsing), AWS Config |
| 3 | **Interface CLI com Argumentos** | MUST HAVE | Baixo | Python (Argparse/Click) |
| 4 | **Coleta de Métricas (Invocations + LastModified)** | MUST HAVE | Médio | Python (Boto3, CloudWatch API) |
| 5 | **Auditoria de Triggers (Event Sources)** | MUST HAVE | Médio | Python (Boto3, Lambda API) |
| 6 | **Tratamento de Erros e Log em Console** | MUST HAVE | Baixo | Python (Logging, Exception Handling) |
| 7 | **Relatório Excel Multi-abas (Contas + Exceptions)** | MUST HAVE | Médio | Python (Pandas/OpenPyXL) |
| 8 | **Argumento `--limit` (Dry Run)** | MUST HAVE | Baixo | Python Logic |
| 9 | **Argumento `--days` (Janela Configurável)** | MUST HAVE | Baixo | Python Logic |

## Requisitos Não-Funcionais (Priorização)

| ID | Requisito Não-Funcional | Classificação (MoSCoW) | Esforço Estimado |
|:---|:---|:---|:---|
| RNF01 | **Processamento Sequencial** | MUST HAVE | Baixo |
| RNF02 | **Feedback Visual de Progresso** | MUST HAVE | Baixo |
| RNF03 | **Mecanismo de Retry (AWS Standard)** | MUST HAVE | Baixo |
| RNF04 | **Output de Erros para Retry (JSON)** | MUST HAVE | Baixo |
| RNF05 | **Compatibilidade Linux (Cross-platform)** | MUST HAVE | Baixo |
| RNF07 | **Segurança de Credenciais (No Hardcode)** | MUST HAVE | N/A (Boas Práticas) |

## Resumo do Escopo MVP
Todas as features listadas acima foram classificadas como **MUST HAVE** para atender ao objetivo core do MVP: auditar, com precisão, o status real das Lambdas e entregar um relatório acionável, tolerando falhas pontuais sem abortar o processo.
