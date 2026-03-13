from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import json

# Criando o especialista em pele e cobertura
base_makeup_agent = Agent(
    name="base_makeup_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Sugere produtos de cobertura de pele, como base, corretivo e contorno.",
    instruction=(
        "Você é um maquiador especialista em pele perfeita. "
        "Baseado no tipo de pele e na ocasião, sugira de 2 a 3 produtos ou técnicas para a base da maquiagem "
        "(ex: base matte ou glow, corretivo, pó selador, contorno). Para cada sugestão, dê um nome, "
        "uma breve descrição de como aplicar e o acabamento esperado."
    )
)

session_service = InMemorySessionService()
runner = Runner(
    agent=base_makeup_agent,
    app_name="base_makeup_app",
    session_service=session_service
)
USER_ID = "user_base_makeup"
SESSION_ID = "session_base_makeup"

async def execute(request):
    session_service.create_session(
        app_name="base_makeup_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    
    skin_type = request.get('skin_type', 'normal')
    occasion = request.get('occasion', 'dia a dia')
    
    prompt = (
        f"O usuário tem pele do tipo '{skin_type}' e precisa de uma maquiagem para '{occasion}'. "
        f"Sugira 2-3 passos ou produtos para a pele (base, corretivo, pó, etc). "
        f"Responda EXCLUSIVAMENTE em formato JSON, usando a chave 'base_makeup' contendo uma lista com as dicas."
    )
    
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            try:
                parsed = json.loads(response_text)
                if "base_makeup" in parsed and isinstance(parsed["base_makeup"], list):
                    return {"base_makeup": parsed["base_makeup"]}
                else:
                    return {"base_makeup": response_text}
            except json.JSONDecodeError:
                return {"base_makeup": response_text}