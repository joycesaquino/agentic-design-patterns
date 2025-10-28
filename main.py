"""
Agentic Design Patterns - Projeto de Demonstração

Este projeto demonstra diferentes padrões arquiteturais para construção
de agentes de IA usando conceitos de engenharia de software.

Estrutura do Projeto:
    /ai_core/              → Configuração centralizada de LLM
    /prompt_chaining/      → Implementação do padrão Pipeline
    /routing/              → Implementação do padrão Routing
    /ai_chat/              → Interface de chat interativa (Chainlit)
    
Requisitos:
    pip install -r requirements.txt

Ambiente:
    - OPENAI_API_KEY: Sua chave da API OpenAI
    - LLM_MODEL (opcional): Modelo a usar (default: gpt-4o-mini)
    - LLM_TEMPERATURE (opcional): Temperatura (default: 0.2)

Execução:
    Para experimentar os padrões de forma interativa, use a interface de chat:
    
    cd ai_chat
    chainlit run app.py
    
    A interface permite alternar entre diferentes chat profiles:
    - 🎬 Prompt Chaining: Recomendador de séries de TV
    - 🏥 Routing: Triagem médica inteligente
"""
from __future__ import annotations

import sys


def main() -> None:
    """Ponto de entrada principal da aplicação."""
    print("\n" + "="*70)
    print("AGENTIC DESIGN PATTERNS")
    print("="*70)
    
    print("\n📚 Padrões Implementados:\n")
    print("  1. Prompt Chaining - Pipeline de recomendação de séries")
    print("  2. Routing - Roteador de triagem médica\n")
    
    print("🚀 Para experimentar os padrões de forma interativa:\n")
    print("  cd ai_chat")
    print("  chainlit run app.py\n")
    
    print("💡 A interface permite alternar entre diferentes chat profiles,")
    print("   cada um demonstrando um padrão de design específico.\n")
    
    print("📖 Documentação:")
    print("  - Prompt Chaining: prompt_chaining/prompt_chaining.md")
    print("  - Routing: routing/routing.md")
    print("  - README.md: Visão geral do projeto\n")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
