import os
import sys
import chainlit as cl
from langchain_core.runnables import RunnableConfig

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ai_core import build_llm
from prompt_chaining import TVSeriesRecommender
from routing import MedicalRouter


@cl.set_chat_profiles
async def chat_profile():
  return [
    cl.ChatProfile(
        name="Prompt Chaining",
        markdown_description="**Recomendador de Séries de TV**\n\n"
                             "Demonstra o padrão *Prompt Chaining* (Pipeline):\n"
                             "1. Extrai critérios do seu texto\n"
                             "2. Gera recomendação personalizada",
    ),
    cl.ChatProfile(
        name="Routing",
        markdown_description="**Triagem Médica Inteligente**\n\n"
                             "Demonstra o padrão *Routing*:\n"
                             "- Analisa sua consulta médica\n"
                             "- Roteia para especialidade apropriada\n"
                             "- 5 especialidades: Pediatria, Nutrologia, Psicologia, Fisioterapia, Default",
    ),
  ]


@cl.on_chat_start
async def start():
  profile = cl.user_session.get("chat_profile")
  llm, langfuse_handler = build_llm()

  if cl.context.session:
    langfuse_handler.set_session_id(cl.context.session.id)

  cl.user_session.set("langfuse_handler", langfuse_handler)

  if profile == "Prompt Chaining":
    recommender = TVSeriesRecommender(llm)
    cl.user_session.set("agent", recommender)
    cl.user_session.set("agent_type", "prompt_chaining")

    await cl.Message(
        content="🎬 **Bem-vindo ao Recomendador de Séries!**\n\n"
                "Descreva o tipo de série que você procura (gênero, temas, duração, ano) "
                "e vou sugerir algo perfeito para você!\n\n"
                "**Exemplo:** *\"Queria ver uma série de ficção científica que tenha mistério, "
                "tipo Black Mirror, mas que não seja muito longa.\"*"
    ).send()

  if profile == "Routing":
    router = MedicalRouter(llm)
    cl.user_session.set("agent", router)
    cl.user_session.set("agent_type", "routing")

    specialties = ", ".join(router.get_available_routes())
    await cl.Message(
        content=f"🏥 **Bem-vindo à Triagem Médica Virtual!**\n\n"
                f"Descreva seus sintomas ou consulta médica e vou direcioná-lo "
                f"para a especialidade apropriada.\n\n"
                f"**Especialidades disponíveis:** {specialties}\n\n"
                f"**Exemplo:** *\"Meu filho de 3 anos está com febre alta e tosse há dois dias.\"*"
    ).send()


@cl.on_message
async def main(message: cl.Message):
  agent_type = cl.user_session.get("agent_type")
  agent = cl.user_session.get("agent")

  handler = cl.user_session.get("langfuse_handler")

  if not agent or not handler:
    await cl.Message(
      content="Erro: Agente ou rastreador não inicializado. Por favor, reinicie o chat.").send()
    return

  config = RunnableConfig(callbacks=[handler])

  msg = cl.Message(content="")
  await msg.send()

  if agent_type == "prompt_chaining":
    criteria = agent.extract_criteria(message.content, config=config)
    await msg.stream_token(f"**Critérios identificados:**\n{criteria}\n\n")

    result = agent.recommend(message.content, config=config)
    await msg.stream_token(f"**Recomendação:**\n{result['recommendation']}")

  if agent_type == "routing":
    result = agent.route(message.content, config=config)
    route_name = result['selected_route'].capitalize()
    await msg.stream_token(f"**Especialidade:** {route_name}\n\n")
    await msg.stream_token(
      f"**Resposta do especialista:**\n{result['response']}")

  await msg.update()


@cl.on_chat_end
def end_chat():
  handler = cl.user_session.get("langfuse_handler")
  if handler:
    print("Finalizando sessão e enviando dados para o Langfuse.")
    handler.flush()