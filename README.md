# Agentic Design Patterns

Demonstração de padrões arquiteturais para construção de agentes de IA usando conceitos de engenharia de software.

## Estrutura do Projeto

```
agentic-design-patterns/
│
├── ai_core/                   # Infraestrutura compartilhada
│   ├── __init__.py
│   └── llm_config.py          # Configuração de LLM
│
├── prompt_chaining/           # Padrão: Prompt Chaining
│   ├── __init__.py
│   ├── prompt_chaining.md
│   └── tv_series_recommender.py
│
├── ai_chat/                   # Interface de chat (Chainlit)
│   └── app.py
│
├── main.py                    # Entry point (CLI)
├── docker-compose.yml         # Docker Compose
└── requirements.txt
```

## Quick Start

### Configuração Inicial

```bash
# 1. Editar arquivo .env com sua API key
nano .env

# Ou criar a partir do exemplo
cp .env.example .env
# Depois edite o .env com seus valores
```

### Opção 1: CLI (Terminal)

```bash
pip install -r requirements.txt
set -a; source .env; set +a
export OPENAI_API_KEY='sk-...'
python main.py
```

### Opção 2: Chat Interface (Chainlit + Docker)

```bash
docker-compose up
# Acessar: http://localhost:8000
```

### Opção 3: Chat Interface (Local)

```bash
pip install -r requirements.txt

set -a; source .env; set +a

cd ai_chat
chainlit run app.py
```

## Padrões Implementados

### Prompt Chaining

Decompõe tarefas complexas em etapas sequenciais.

📖 Documentação: [`prompt_chaining/prompt_chaining.md`](./prompt_chaining/prompt_chaining.md)

## GitHub Actions

O projeto está configurado com CI/CD usando GitHub Actions:

- **CI**: Lint, testes e build Docker em cada push/PR
- **Docker Publish**: Publica imagem no GitHub Container Registry em tags

### Configurar Secrets

1. Acesse: `Settings` → `Secrets and variables` → `Actions`
2. Adicione os secrets:
   - `OPENAI_API_KEY` (obrigatório)
3. Adicione variables opcionais:
   - `LLM_MODEL` (padrão: gpt-4o-mini)
   - `LLM_TEMPERATURE` (padrão: 0.2)

📖 Detalhes: [`.github/SECRETS.md`](./.github/SECRETS.md)
