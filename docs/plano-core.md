# Plano Core (Base Framework)

## CLI Skeleton
- [ ] Implementar `src/crawler/main.py` usando `click`
- [ ] Configurar argumentos: `--input`, `--days` (default 180), `--limit`
- [ ] Configurar Logger global para logs no console e/ou arquivo

## Domain Models
- [ ] Definir Dataclass `InputItem`
- [ ] Definir Dataclass `LambdaResult`

## AWS Session Management
- [ ] Implementar `services/profiles.py` para ler `~/.aws/config` e montar dicionário `AccountID -> ProfileName`
- [ ] Implementar factory em `services/aws.py` que cria sessões `boto3.Session(profile_name=...)` dinamicamente

## IO Adapters
- [ ] Implementar `adapters/storage.py` para ler JSON e validar schema básico
- [ ] Criar estrutura inicial do `orchestrator.py` que apenas lê o input, itera e loga no console (sem chamar AWS ainda)
