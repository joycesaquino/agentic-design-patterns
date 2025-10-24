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
├── routing/                   # Padrão: Routing
│   ├── __init__.py
│   ├── routing.md
│   └── routing_example.py
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
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar variáveis de ambiente
# Editar arquivo .env com sua API key
nano .env

# Ou criar a partir do exemplo
cp .env.example .env
# Depois edite o .env com seus valores
```

### Opção 1: Chat Interface (Local) - Recomendado

A melhor forma de experimentar os padrões é através da interface de chat interativa:

```bash
# Carregar variáveis de ambiente
set -a; source .env; set +a

# Iniciar a interface de chat
cd ai_chat
chainlit run app.py
```

A interface permite alternar entre **Chat Profiles**:
- 🎬 **Prompt Chaining**: Recomendador de séries de TV
- 🏥 **Routing**: Triagem médica inteligente

### Opção 2: Chat Interface (Docker)

```bash
docker-compose up
# Acessar: http://localhost:8000
```

## Padrões Implementados

Todos os padrões podem ser testados de forma interativa através da interface de chat (`ai_chat/app.py`).

### 1. Prompt Chaining

Decompõe tarefas complexas em etapas sequenciais (pipeline).

**Exemplo Interativo:** 🎬 Recomendador de séries de TV
- Etapa 1: Extrai critérios do texto livre do usuário
- Etapa 2: Gera recomendação personalizada baseada nos critérios
- Interface mostra cada etapa do pipeline em tempo real

📖 Documentação: [`prompt_chaining/prompt_chaining.md`](./prompt_chaining/prompt_chaining.md)  
💻 Código: [`prompt_chaining/tv_series_recommender.py`](./prompt_chaining/tv_series_recommender.py)

### 2. Routing

Sistema de tomada de decisão dinâmico que analisa a entrada e direciona para a rota especializada apropriada.

**Exemplo Interativo:** 🏥 Triagem Médica Inteligente
- Analisa a consulta médica do paciente em linguagem natural
- Roteia dinamicamente para a especialidade apropriada
- 5 especialidades: Pediatria (👶), Nutrologia (🥗), Psicologia (🧠), Fisioterapia (🏃), Default (💬)
- Cada especialidade tem seu próprio prompt, tom de voz e personalidade

📖 Documentação: [`routing/routing.md`](./routing/routing.md)  
💻 Código: [`routing/routing_example.py`](routing/medical_router.py)

### Como Testar

1. Inicie a interface: `cd ai_chat && chainlit run app.py`
2. Selecione um **Chat Profile** no menu superior
3. Interaja com o padrão em tempo real

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
