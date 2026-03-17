from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import json
import os
from google.adk.agents import Agent

os.environ["OPENAI_API_KEY"] = "" 

extractor_agent = Agent(
    name="clinical_extractor_agent",
    model=LiteLlm("openai/gpt-4o"), 
    description="Extrai entidades clínicas de transcrições médicas.",
    instruction=(
        "Você é um especialista em processamento de linguagem natural médica. "
        "Dada uma transcrição médica, extraia as seguintes entidades: "
        "Sintomas, Diagnósticos, Medicamentos e Procedimentos. "
        "Responda EXCLUSIVAMENTE em formato JSON contendo essas 4 chaves como listas de strings."
    )
)

session_service = InMemorySessionService()
runner = Runner(agent=extractor_agent, app_name="extractor_app", session_service=session_service)
USER_ID = "med_system"
SESSION_ID = "extract_session"

async def execute(request):
    session_service.create_session(app_name="extractor_app", user_id=USER_ID, session_id=SESSION_ID)
    prompt = f"Extraia as entidades da seguinte transcrição: '{request.get('transcription_text')}'"
    
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            try:
                return {"extracted_data": json.loads(event.content.parts[0].text)}
            except:
                return {"extracted_data": event.content.parts[0].text}