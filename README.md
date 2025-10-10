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
├── main.py                     # Entry point
└── requirements.txt
```

## Quick Start

### Instalação

```bash
pip install -r requirements.txt
```

### Configuração

```bash
export OPENAI_API_KEY='sk-...'
```

### Execução

```bash
python main.py
```

## Padrões Implementados

### Prompt Chaining

Decompõe tarefas complexas em etapas sequenciais.

📖 Documentação: [`prompt_chaining/prompt_chaining.md`](./prompt_chaining/prompt_chaining.md)
