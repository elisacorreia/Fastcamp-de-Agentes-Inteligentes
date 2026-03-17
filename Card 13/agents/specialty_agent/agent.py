from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import json

specialty_agent = Agent(
    name="specialty_classifier_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Classifica a especialidade médica baseada na transcrição.",
    instruction=(
        "Você é um médico triador chefe. Dada uma transcrição médica, classifique a "
        "qual Especialidade Médica principal este caso pertence (ex: Cardiologia, Ortopedia, Cirurgia Geral). "
        "Forneça também uma breve justificativa de 1 frase. "
        "Responda EXCLUSIVAMENTE em JSON com as chaves 'especialidade' e 'justificativa'."
    )
)

session_service = InMemorySessionService()
runner = Runner(agent=specialty_agent, app_name="specialty_app", session_service=session_service)
USER_ID = "med_system"
SESSION_ID = "specialty_session"

async def execute(request):
    session_service.create_session(app_name="specialty_app", user_id=USER_ID, session_id=SESSION_ID)
    prompt = f"Classifique a especialidade desta transcrição: '{request.get('transcription_text')}'"
    
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            try:
                return {"classification": json.loads(event.content.parts[0].text)}
            except:
                return {"classification": event.content.parts[0].text}