"""
TV Series Recommender - Exemplo de Prompt Chaining

Este módulo implementa um recomendador de séries de TV usando o padrão
de Prompt Chaining (Pipeline):

1. Extração: Identifica critérios de busca a partir de texto livre
2. Transformação: Gera recomendação personalizada baseada nos critérios

Arquitetura:
    User Input → [extraction_chain] → Criteria → [transform_chain] → Recommendation
"""
from __future__ import annotations

import sys
from typing import Any, Dict

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
    - Stage 2 (Transformation): Gera recomendação personalizada
    """
    
    def __init__(self, llm: Any):
        self.llm = llm
        self._setup_chains()
    
    def _setup_chains(self) -> None:
        # Stage 1: Extraction Chain
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
        
        # Stage 2: Transformation Chain
        self.prompt_transform = ChatPromptTemplate.from_template(
            "Com base nos critérios de busca abaixo, sugira 1 série específica "
            "e escreva uma pequena sinopse do porquê o usuário vai gostar dela.\n\n"
            "Critérios: {search_criteria}"
        )
        
        # Full Pipeline: input → extraction → transformation → output
        self.full_chain = (
            {"search_criteria": self.extraction_chain}
            | self.prompt_transform
            | self.llm
            | StrOutputParser()
        )
    
    def extract_criteria(self, text_input: str) -> str:
        """
        Extrai critérios de busca do texto livre do usuário.
        
        Args:
            text_input: Descrição em texto livre do que o usuário procura
            
        Returns:
            str: Critérios estruturados extraídos
        """
        return self.extraction_chain.invoke({"text_input": text_input})
    
    def recommend(self, text_input: str) -> Dict[str, str]:
        """
        Gera uma recomendação completa a partir de texto livre.
        
        1. Extrai critérios do texto
        2. Gera recomendação baseada nos critérios
        
        Args:
            text_input: Descrição em texto livre do que o usuário procura
            
        Returns:
            Dict com 'criteria' (extraído) e 'recommendation' (final)
        """
        criteria = self.extract_criteria(text_input)
        recommendation = self.full_chain.invoke({"text_input": text_input})
        
        return {
            "criteria": criteria,
            "recommendation": recommendation
        }


def run_example(llm: Any) -> None:
    """
    Executa o exemplo de recomendação de séries.
    
    Args:
        llm: Instância configurada de LLM
    """
    recommender = TVSeriesRecommender(llm)
    
    # Input de exemplo
    input_text = (
        "Queria ver uma série de ficção científica que tenha mistério, "
        "tipo Black Mirror, mas que não seja muito longa. "
        "E que seja mais nova, dos últimos 2 anos."
    )
    
    print("\n" + "="*70)
    print("EXEMPLO: TV Series Recommender - Prompt Chaining")
    print("="*70)
    
    print("\n[ENTRADA DO USUÁRIO]")
    print(f'"{input_text}"')
    
    # Executar pipeline
    result = recommender.recommend(input_text)
    
    print("\n[ETAPA 1: CRITÉRIOS EXTRAÍDOS]")
    print(result["criteria"])
    
    print("\n[ETAPA 2: RECOMENDAÇÃO FINAL]")
    print(result["recommendation"])
    
    print("\n" + "="*70)

