# Importando as ferramentas necessárias para criar o agente e lidar com os dados
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import json

# Criando o nosso especialista em cuidados com a pele
skincare_agent = Agent(
    name="skincare_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Sugere a rotina de preparação da pele antes da maquiagem.",
    instruction=(
        "Você é um dermatologista e especialista em preparação de pele (skincare) pré-maquiagem. "
        "Baseado no tipo de pele do usuário e na ocasião, sugira de 2 a 3 passos essenciais "
        "(ex: limpeza, hidratação, protetor solar, primer). Para cada passo, dê um nome, "
        "uma breve descrição e o motivo de ser importante. Responda de forma clara e estruturada."
    )
)

session_service = InMemorySessionService()
runner = Runner(
    agent=skincare_agent,
    app_name="skincare_app",
    session_service=session_service
)
USER_ID = "user_skincare"
SESSION_ID = "session_skincare"

# A função 'async' (assíncrona) permite que o Python faça outras coisas enquanto espera a IA responder
async def execute(request):
    session_service.create_session(
        app_name="skincare_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    
    # Pegando as informações enviadas pelo (host_agent)
    skin_type = request.get('skin_type', 'normal')
    occasion = request.get('occasion', 'dia a dia')
    
    # Montando a pergunta (prompt) para a IA em português
    prompt = (
        f"O usuário tem pele do tipo '{skin_type}' e está se preparando para a ocasião '{occasion}'. "
        f"Sugira 2-3 passos de skincare pré-maquiagem. "
        f"Responda EXCLUSIVAMENTE em formato JSON, usando a chave 'skincare' contendo uma lista com os passos."
    )
    
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    
    # Enviando a mensagem e aguardando a resposta
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            try:
                # O json.loads transforma o texto da IA em um 'dicionário' que o Python consegue ler facilmente
                parsed = json.loads(response_text)
                if "skincare" in parsed and isinstance(parsed["skincare"], list):
                    return {"skincare": parsed["skincare"]}
                else:
                    return {"skincare": response_text}
            except json.JSONDecodeError:
                # Se der erro na leitura do JSON, retornamos o texto puro
                return {"skincare": response_text}