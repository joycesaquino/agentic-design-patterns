"""
Agentic Design Patterns - Demonstração Executável

Este script demonstra diferentes padrões arquiteturais para construção
de agentes de IA, começando com Prompt Chaining.

Estrutura do Projeto:
    /ai-core/              → Configuração centralizada de LLM
    /prompt-chaining/      → Implementação do padrão Pipeline
    
Requisitos:
    pip install -U langchain-core langchain-openai

Ambiente:
    - OPENAI_API_KEY: Sua chave da API OpenAI
    - LLM_MODEL (opcional): Modelo a usar (default: gpt-4o-mini)
    - LLM_TEMPERATURE (opcional): Temperatura (default: 0.2)

Execução:
    python main.py
"""
from __future__ import annotations

import sys

# Imports dos módulos locais
try:
    from ai_core import build_llm
    from prompt_chaining.tv_series_recommender import run_example
except ImportError as e:
    print(
        f"Erro ao importar módulos do projeto: {e}\n\n"
        "Certifique-se de estar executando do diretório raiz do projeto.\n",
        file=sys.stderr,
    )
    sys.exit(1)


def main() -> None:
    """Ponto de entrada principal da aplicação."""
    print("\n" + "="*70)
    print("AGENTIC DESIGN PATTERNS - Demonstração")
    print("="*70)
    print("\nPadrão demonstrado: PROMPT CHAINING (Pipeline)\n")
    
    # Inicializar LLM através do módulo centralizado
    print("Inicializando LLM...")
    llm = build_llm()
    print(f"✓ LLM configurado: {llm.model_name} (temperature={llm.temperature})\n")
    
    # Executar exemplo de Prompt Chaining
    run_example(llm)
    
    print("\n✓ Demonstração concluída com sucesso!\n")


if __name__ == "__main__":
    main()
