# Requisitos Não-Funcionais (RNF)

## Performance e Concorrência
- **RNF01 - Processamento Sequencial:** Dado o volume médio (~700 lambdas) e a não criticidade de tempo, o processamento será sequencial (single-threaded) para priorizar estabilidade e simplicidade de debugging.
- **RNF02 - Feedback de Progresso:** O sistema deve exibir indicadores de progresso claros no console (ex: contador `Processando 10/700 - NomeDaLambda`) para que o operador saiba que o script não travou.

## Resiliência e Continuidade
- **RNF03 - Mecanismo de Retry em Falhas:** O sistema não deve ter rate-limiting complexo, confiando no backoff padrão da AWS. No entanto, falhas de API não devem abortar a execução total.
- **RNF04 - Arquivo de Estado de Erros (Resume Capability):** Ao final da execução, se houver falhas, gerar um arquivo JSON separado (`errors.json`) contendo apenas os itens que falharam. Isso permitirá reexecutar o script usando este arquivo como novo input, evitando reprocessar o que já deu certo.

## Portabilidade e Compatibilidade
- **RNF05 - Cross-Platform (Windows Dev / Linux Prod):** O código deve ser agnóstico de sistema operacional, utilizando caminhos de arquivo relativos e bibliotecas compatíveis com ambos os OSs.
- **RNF06 - Gerenciamento de Dependências:** Uso estrito do `uv` e `venv` para garantir que o ambiente seja reprodutível em Linux sem conflitos de pacotes globais.

## Segurança
- **RNF07 - Princípio do Menor Privilégio (Cliente):** A ferramenta não gerencia credenciais, apenas utiliza sessões ativas/configuradas no ambiente. Não deve haver hardcode de chaves.
- **RNF08 - Tratamento de Dados Sensíveis:** O relatório final não deve expor Conteúdo da Lambda ou Variáveis de Ambiente, apenas metadados e contagens.
