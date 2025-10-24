"""
Medical Triage Router - Exemplo de Routing baseado em LLM.

Este módulo implementa um sistema de triagem médica que direciona consultas
de pacientes para a especialidade médica apropriada usando um LLM como roteador.

Arquitetura:
    User Query → [Router LLM] → Specialty Selection → [Specialized Agent] → Response

Padrão de Design:
    - Strategy Pattern: Cada especialidade é uma estratégia com seu próprio prompt
    - Router Pattern: LLM analisa a entrada e seleciona dinamicamente a especialidade
"""
from __future__ import annotations

import sys
from typing import Any, Dict, List, Optional

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

from . import prompts


class RouteDefinition:
    """Define uma rota específica no sistema de roteamento."""
    
    def __init__(self, name: str, description: str, keywords: Optional[List[str]] = None):
        self.name = name
        self.description = description
        self.keywords = keywords or []
    
    def __repr__(self) -> str:
        return f"Route(name='{self.name}')"


class IntelligentRouter:
    """
    Roteador inteligente baseado em LLM.
    
    Analisa a entrada do usuário usando um LLM para decidir qual rota
    especializada deve processar a requisição.
    """
    
    def __init__(self, llm: Any):
        self.llm = llm
        self.routes: List[RouteDefinition] = []
        self.route_chains: Dict[str, Any] = {}
        self.router_chain = None
    
    def _setup_routes(self) -> None:
        raise NotImplementedError("Not implemented for this router")
    
    def _get_routes_description(self) -> str:
        """Retorna a descrição formatada de todas as rotas disponíveis."""
        return "\n".join([
            f"- {route.name}: {route.description}"
            for route in self.routes
        ])
    
    def _create_chain(self, template: str) -> Any:
        """
        Cria uma chain do LangChain a partir de um template.
        
        Args:
            template: Template de prompt a ser usado
            
        Returns:
            Chain configurada (prompt | llm | parser)
        """
        prompt = ChatPromptTemplate.from_template(template)
        return prompt | self.llm | StrOutputParser()
    
    def _setup_router_chain(self) -> None:
        """Cria a chain de roteamento que usa o LLM para selecionar a rota."""
        self.router_chain = self._create_chain(prompts.ROUTER_TEMPLATE)
    
    def _setup_route_chains(self) -> None:
        raise NotImplementedError("Not implemented for this router")
    
    def _execute_route(self, route_name: str, user_input: str) -> str:
        """Executa a chain associada à rota selecionada."""
        route_name = route_name.strip().lower()
        
        if route_name not in self.route_chains:
            print(f"Especialidade '{route_name}' não encontrada. Usando rota 'default'.")
            route_name = "default"
        
        chain = self.route_chains[route_name]
        return chain.invoke({"user_input": user_input})
    
    def route(self, user_input: str) -> Dict[str, Any]:
        """Processa a entrada do usuário através do sistema de roteamento."""
        selected_route = self.router_chain.invoke({
            "routes_description": self._get_routes_description(),
            "user_input": user_input
        })
        
        response = self._execute_route(selected_route, user_input)
        
        return {
            "selected_route": selected_route.strip().lower(),
            "response": response
        }
    
    def get_available_routes(self) -> List[str]:
        return [route.name for route in self.routes]


class MedicalRouter(IntelligentRouter):
    """
    Roteador de Triagem Médica.
    
    Implementação concreta do IntelligentRouter que direciona consultas de pacientes
    para 5 especialidades médicas: Pediatria, Nutrologia, Psicologia, Fisioterapia
    e uma rota Default para casos gerais.
    """
    
    def __init__(self, llm: Any):
        """
        Inicializa o roteador de triagem e configura todas as rotas e chains.
        
        Args:
            llm: Instância configurada de LLM
        """
        super().__init__(llm)
        self._setup_routes()
        self._setup_router_chain()
        self._setup_route_chains()
        
    def _setup_routes(self) -> None:
        """
        Define as especialidades médicas disponíveis.
        
        Cada RouteDefinition contém:
        - name: Identificador da especialidade
        - description: Descrição clara para o LLM entender quando usar esta rota
        - keywords: Palavras-chave associadas (para documentação)
        """
        self.routes = [
            RouteDefinition(
                name="pediatria",
                description="Responde a perguntas sobre saúde infantil, bebês, vacinação, desenvolvimento e doenças em crianças.",
                keywords=["filho", "bebê", "criança", "febre", "vacina"]
            ),
            RouteDefinition(
                name="nutrologia", 
                description="Lida com questões de dieta, alimentação, nutrição, perda ou ganho de peso e suplementação vitamínica.",
                keywords=["dieta", "emagrecer", "peso", "alimentação", "vitamina"]
            ),
            RouteDefinition(
                name="psicologia", 
                description="Trata de consultas sobre saúde mental, ansiedade, depressão, estresse, terapia e bem-estar emocional.",
                keywords=["ansiedade", "triste", "estresse", "terapia", "sentimentos"]
            ),
            RouteDefinition(
                name="fisioterapia", 
                description="Focado em dor física, reabilitação de lesões, problemas musculares, ósseos ou de movimento.",
                keywords=["dor", "joelho", "costas", "lesão", "torção"]
            ),
            RouteDefinition(
                name="default", 
                description="Responde a saudações gerais ou perguntas que não se encaixam nas outras especialidades.",
                keywords=["oi", "obrigado", "bom dia"]
            ),
        ]

    def _setup_route_chains(self) -> None:
        """
        Configura as chains especializadas para cada especialidade.
        
        Cada especialidade tem:
        - Um prompt personalizado com tom e foco específicos
        - Uma chain (prompt | llm | parser) dedicada
        
        Usa o dicionário SPECIALTY_TEMPLATES do módulo prompts para criar
        as chains de forma dinâmica e sem repetição de código.
        """
        self.route_chains = {
            specialty: self._create_chain(template)
            for specialty, template in prompts.SPECIALTY_TEMPLATES.items()
        }
