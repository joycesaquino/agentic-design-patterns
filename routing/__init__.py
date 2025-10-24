"""
Routing - Padrão de Tomada de Decisão Dinâmica para agentes de IA.

Este módulo implementa o padrão Routing, que permite a um agente de IA
escolher dinamicamente entre múltiplas rotas/ações baseado no contexto
da entrada do usuário.
"""
from .medical_router import IntelligentRouter, RouteDefinition, MedicalRouter

__all__ = ["IntelligentRouter", "RouteDefinition", "MedicalRouter"]


