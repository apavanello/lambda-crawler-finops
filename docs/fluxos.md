# Fluxos Principais

## Fluxo Geral de Execução

```mermaid
flowchart TD
    Start([Início]) --> LoadConfig[Ler ~/.aws/config e Cachear Profiles]
    LoadConfig --> ReadInput[Ler JSON de Input]
    ReadInput --> Validate{JSON Válido?}
    Validate -- Não --> Exit([Fim com Erro])
    Validate -- Sim --> LoopStart[Iniciar Loop de Itens]
    
    LoopStart --> CheckLimit{Atingiu Limite?}
    CheckLimit -- Sim --> GenerateReport
    CheckLimit -- Não --> NextItem[Pegar Próxima Lambda]
    
    NextItem --> FindProfile[Buscar Profile p/ Account ID]
    FindProfile --> HasProfile{Profile Encontrado?}
    
    HasProfile -- Não --> LogErrProfile[Logar Erro: Profile Missing]
    LogErrProfile --> StoreError[Adicionar à Lista de Erros]
    StoreError --> LoopStart
    
    HasProfile -- Sim --> CreateSession[Criar Sessão Boto3]
    CreateSession --> CallGetFunc[AWS: GetFunction (Config)]
    CallGetFunc --> SuccessFunc{Sucesso?}
    
    SuccessFunc -- Não --> LogErrAWS[Logar Erro AWS]
    LogErrAWS --> StoreError
    
    SuccessFunc -- Sim --> CallMetrics[AWS: GetMetricStatistics (CloudWatch)]
    CallMetrics --> CallTriggers[AWS: ListEventSourceMappings]
    CallTriggers --> ProcessData[Processar/Consolidar Dados]
    ProcessData --> StoreSuccess[Adicionar à Lista de Sucesso]
    StoreSuccess --> LoopStart
    
    GenerateReport[Gerar Excel Multi-abas] --> SaveErrors[Salvar errors.json]
    SaveErrors --> End([Fim])
```
