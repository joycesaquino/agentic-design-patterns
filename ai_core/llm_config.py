from __future__ import annotations

import os
import sys
from typing import Optional


def build_llm(model: Optional[str] = None, temperature: Optional[float] = None):
    """Instantiate an OpenAI chat model via langchain-openai.

    Reads OPENAI_API_KEY from env. Allows overriding model and temperature.
    
    Args:
        model: Nome do modelo OpenAI (padrão: gpt-4o-mini ou valor de LLM_MODEL env var)
        temperature: Temperatura para geração (padrão: 0.2 ou valor de LLM_TEMPERATURE env var)
        
    Returns:
        ChatOpenAI: Instância configurada do modelo
        
    Raises:
        SystemExit: Se dependências não estiverem instaladas ou OPENAI_API_KEY não estiver definida
    """
    try:
        import importlib
        openai_mod = importlib.import_module('langchain_openai')
        ChatOpenAI = getattr(openai_mod, 'ChatOpenAI')
    except Exception as e:
        print(
            "Missing 'langchain-openai'. Install with:\n"
            "  pip install -U langchain-openai\n\n"
            f"Original import error: {e}\n",
            file=sys.stderr,
        )
        sys.exit(1)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(
            "Error: OPENAI_API_KEY is not set. Please export your OpenAI API key, e.g.:\n"
            "  export OPENAI_API_KEY='sk-...'\n",
            file=sys.stderr,
        )
        sys.exit(2)

    model_name = model or os.getenv("LLM_MODEL", "gpt-4o-mini")
    try:
        temp_val = float(temperature) if temperature is not None else float(os.getenv("LLM_TEMPERATURE", "0.2"))
    except ValueError:
        temp_val = 0.2

    # ChatOpenAI uses OPENAI_API_KEY from the environment automatically
    return ChatOpenAI(model=model_name, temperature=temp_val)

