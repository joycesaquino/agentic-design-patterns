import os
import sys
import chainlit as cl

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ai_core import build_llm
from prompt_chaining import TVSeriesRecommender


@cl.on_chat_start
async def start():
    """Initialize chat session with LLM and recommender."""
    # Build LLM
    llm = build_llm()
    
    # Create recommender
    recommender = TVSeriesRecommender(llm)
    
    # Store in session
    cl.user_session.set("recommender", recommender)
    
    # Welcome message
    await cl.Message(
        content="Oi! Sou seu assistente de recomendação de séries.\n\n"
                "Descreva o tipo de série que você procura"
                "e vou sugerir algo perfeito para você!"
    ).send()


@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages and generate recommendations."""
    # Get recommender from session
    recommender = cl.user_session.get("recommender")
    
    # Show thinking message
    msg = cl.Message(content="")
    await msg.send()
    
    # Extract criteria
    criteria = recommender.extract_criteria(message.content)
    await msg.stream_token(f"**Critérios identificados:**\n{criteria}\n\n")
    
    # Generate recommendation
    result = recommender.recommend(message.content)
    await msg.stream_token(f"**Recomendação:**\n{result['recommendation']}")

    await msg.update()

