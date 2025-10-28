from __future__ import annotations

import sys
from typing import Any, Dict

from langchain_core.runnables import RunnableConfig

try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
except Exception as e:
    missing = (
      "Missing required packages. Install with:\n"
      "  pip install -U langchain-core langchain-openai\n\n"
      f"Original import error: {e}\n"
    )
    print(missing, file=sys.stderr)
    sys.exit(1)


class TVSeriesRecommender:
  """
  Recomendador de séries usando Prompt Chaining.

  Implementa um pipeline de dois estágios:
  - Stage 1 (Extraction): Extrai critérios estruturados do texto livre
  - Stage 2 (Recommendation): Gera recomendação personalizada a partir dos critérios
  """

  def __init__(self, llm: Any):
    self.llm = llm
    self._setup_chains()

  def _setup_chains(self) -> None:
    self.prompt_extract = ChatPromptTemplate.from_template(
        "Extraia os critérios para encontrar uma série do texto a seguir: "
        "gênero principal, subgênero ou tema, exemplos, restrição de duração "
        "e ano de lançamento.\n\nTexto: {text_input}"
    )

    self.extraction_chain = (
        self.prompt_extract
        | self.llm
        | StrOutputParser()
    )

    self.prompt_recommend = ChatPromptTemplate.from_template(
        "Com base nos critérios de busca abaixo, sugira 1 série específica "
        "e escreva uma pequena sinopse do porquê o usuário vai gostar dela.\n\n"
        "Critérios: {search_criteria}"
    )

    self.recommendation_chain = (
        self.prompt_recommend
        | self.llm
        | StrOutputParser()
    )

  def extract_criteria(self, text_input: str, config: RunnableConfig) -> str:
    """
    Extrai critérios de busca do texto livre do usuário.

    Args:
        text_input: Descrição em texto livre do que o usuário procura
        config: [LANGFUSE] Dicionário de configuração para callbacks

    Returns:
        str: Critérios estruturados extraídos
    """
    return self.extraction_chain.invoke(
        {"text_input": text_input},
        config=config
    )

  def recommend(self, criteria: str, config: RunnableConfig) -> str:
    """
    Gera uma recomendação com base nos critérios já extraídos.

    Args:
        criteria: Os critérios já extraídos pelo 'extract_criteria'
        config: [LANGFUSE] Dicionário de configuração para callbacks

    Returns:
        str: A recomendação final
    """
    recommendation = self.recommendation_chain.invoke(
        {"search_criteria": criteria},
        config=config
    )

    return recommendation