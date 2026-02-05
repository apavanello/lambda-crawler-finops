# Plano de Setup de Infraestrutura (CLI Distribution)

## Build e Empacotamento
Como é uma CLI local em Python, a "infra" é a distribuição correta do pacote.

- [ ] Criar script de build no Makefile (limpeza de artifacts, execução de testes)
- [ ] Documentar como rodar em Windows vs Linux no `README.md`
- [ ] (Opcional) Testar criação de executável único (PyInstaller) se desejado no futuro, mas por enquanto focar no run via `uv`.

## Qualidade e CI Ligeiro (Local)
- [ ] Configurar `ruff` (`pyproject.toml`) para regras de linting básicas
- [ ] Garantir que `make setup` instala tudo corretamente em uma máquina limpa

## Documentação de Uso
- [ ] Criar `README.md` com:
  - Pré-requisitos (Python, AWS CLI configurado)
  - Como instalar
  - Exemplos de comando
  - Explicação do Input e Output
