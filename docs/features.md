# Funcionalidades do Projeto (Features)

## 1. Interface de Linha de Comando (CLI) e Confirguração
O sistema deve ser executado via CLI, aceitando argumentos para flexibilizar a execução.
- **Argumentos Suportados:**
  - `--input`: Caminho para o arquivo JSON de entrada (Obrigatório).
  - `--days`: Janela de tempo em dias para busca de métricas (Obrigatório, Default: 180 dias).
  - `--limit`: Limite de itens a serem processados para testes rápidos (Opcional).

## 2. Leitura e Validação de Input
Capacidade de ler arquivos de entrada estruturados.
- Ler arquivo JSON.
- Validar se o JSON contém os campos obrigatórios `name` (Nome da Lambda) e `account` (ID da Conta).
- Reportar erro imediato caso o formato seja inválido.

## 3. Gestão Inteligente de Credenciais AWS SSO
Automação na seleção de credenciais para evitar trocas manuais de contexto.
- Ler o arquivo `~/.aws/config` do usuário.
- Mapear automaticamente o `Account ID` fornecido no input para o `Profile Name` correspondente.
- Instanciar sessões `boto3` dinamicamente usando o profile correto para cada Lambda.

## 4. Coleta de Métricas de Uso (Crawler)
Motor de busca para determinar a realidade de uso do recurso.
- Obter metadados da função (`LastModified`).
- Consultar API do **CloudWatch Metrics** buscar a soma de `Invocations`.
- Respeitar a janela de tempo definida pelo argumento `--days`.
- Identificar se a função teve 0 ou >0 invocações no período.

## 5. Auditoria de Gatilhos (Triggers)
Verificação de pontos de entrada da função.
- Listar *Event Source Mappings* e configurações de gatilhos da Lambda.
- Contabilizar quantidade de triggers ativos.
- Identificar se existe ao menos um trigger habilitado (`Boolean`).

## 6. Tratamento de Erros e Log de Auditoria
Resiliência e rastreabilidade da execução.
- Capturar erros de conexão, permissão ou "Resource Not Found".
- Logar falhas no console (STDERR/STDOUT) em tempo real.
- Não interromper o processamento total em caso de falha individual (Skip & Continue).
- Adicionar registro de falha estruturado para o relatório final.

## 7. Geração de Relatório Excel Consolidado
Exportação rica para análise de FinOps.
- Gerar Arquivo `.xlsx` único.
- **Abas de Conta:** Agrupar lambdas processadas com sucesso em abas separadas por `Account ID`.
- **Aba de Exceções:** Uma aba dedicada ("Exceptions") listando todas as lambdas que falharam, com o motivo do erro.
- Colunas esperadas: Nome, Conta, Região, Última Modificação, Última Invocação (Data), Qtd Invocações (Período), Tem Triggers?, Qtd Triggers.
