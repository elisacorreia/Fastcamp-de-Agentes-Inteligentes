from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

host_agent = Agent(
    name="makeup_host_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Coordena a criação de um look de maquiagem chamando agentes de skincare, base e detalhes.",
    instruction="You are a master makeup artist (host agent). " # Você é um maquiador mestre
                "Your job is to orchestrate a complete makeup routine. " # Seu trabalho é orquestrar a rotina
                "You call external agents for skincare, base makeup, and eye/lip details, then return a final beautiful look."
)
session_service = InMemorySessionService()
runner = Runner(
    agent=host_agent,
    app_name="makeup_host_app",
    session_service=session_service
)
USER_ID = "user_makeup"
SESSION_ID = "session_makeup"

async def execute(request):
    session_service.create_session(
        app_name="makeup_host_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    
    # O prompt agora pede um look de maquiagem em vez de uma viagem
    prompt = (
        f"Crie uma recomendação de maquiagem para a ocasião '{request.get('occasion', 'dia a dia')}' "
        f"para o tipo de pele '{request.get('skin_type', 'mista')}'. "
        f"Chame os agentes de skincare, base e detalhes para obter os resultados."
    )
    
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            return {"summary": event.content.parts[0].text}