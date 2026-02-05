# Plano Funcional: Crawler & Relatórios

## 1. Implementação dos Serviços AWS (`services/aws.py`)
- [ ] Implementar `get_lambda_details(session, function_name)`: Retorna `LastModified` e ARN.
- [ ] Implementar `get_invocation_metrics(session, function_name, days)`: Consulta CloudWatch `GetMetricStatistics` (Sum, Period=86400).
- [ ] Implementar `get_triggers(session, function_name)`: Lista `EventSourceMappings`.

## 2. Orquestração e Lógica de Negócio (`orchestrator.py`)
- [ ] Integrar loop principal com chamadas de serviço.
- [ ] Implementar lógica de fallback: Se falhar, capturar exceção, logar string de erro no objeto resultado e continuar.
- [ ] Implementar barra de progresso simples ou log contador (`[X/Y] Processing...`).

## 3. Geração de Relatório Excel (`adapters/excel.py`)
- [ ] Implementar função que recebe lista de `LambdaResult`.
- [ ] Criar Pandas DataFrame.
- [ ] Agrupar por `AccountID` e escrever em abas diferentes usando `ExcelWriter`.
- [ ] Filtrar falhas e escrever na aba `Exceptions`.

## 4. Retries e Output de Erros
- [ ] No final da orquestração, filtrar lista de erros.
- [ ] Se houver erros, serializar para JSON (`errors.json`).

## 5. Validação e Teste Manual
- [ ] Criar arquivo de input real/mock `data/input_test.json`.
- [ ] Executar contra uma conta real (se disponível) para validar permissões AWS.
- [ ] Validar se Excel abre corretamente e se dados batem com console AWS.
