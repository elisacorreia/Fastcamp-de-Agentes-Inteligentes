from fastapi import FastAPI
from pydantic import BaseModel
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

app = FastAPI()


whatsapp_agent = Agent(
    name="whatsapp_agent",
    model=LiteLlm("openai/gpt-4o"), # Você pode trocar para gemini se preferir
    description="Assistente de atendimento via WhatsApp.",
    instruction="Você é um assistente virtual prestativo que atende clientes via WhatsApp. Suas respostas devem ser curtas, diretas e amigáveis, ideais para leitura no celular."
)


session_service = InMemorySessionService()
runner = Runner(
    agent=whatsapp_agent,
    app_name="whatsapp_app",
    session_service=session_service
)


class MessagePayload(BaseModel):
    phone_number: str
    message: str


@app.post("/chat")
async def chat(payload: MessagePayload):

    user_id = payload.phone_number
    session_id = payload.phone_number 

    try:
        session_service.get_session(app_name="whatsapp_app", session_id=session_id)
        print(f"Sessão existente encontrada para: {session_id}")
    except Exception:
        print(f"Criando nova sessão para: {session_id}")
        session_service.create_session(
            app_name="whatsapp_app",
            user_id=user_id,
            session_id=session_id
        )

 
    new_message = types.Content(role="user", parts=[types.Part(text=payload.message)])
    
    response_text = ""
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=new_message):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            
    return {"response": response_text}

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)