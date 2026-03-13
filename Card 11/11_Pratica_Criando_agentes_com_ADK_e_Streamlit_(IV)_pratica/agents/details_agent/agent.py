# Etapa 1: Importações
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import json

# Etapa 2: Agente de Detalhes (Olhos e Boca)
details_agent = Agent(
    name="details_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Sugere detalhes de maquiagem para olhos e lábios.",
    instruction=(
        "Você é um especialista em maquiagem focado em olhos e lábios. "
        "Dada uma ocasião e o estilo desejado pelo usuário, sugira de 2 a 3 passos ou produtos "
        "para destacar os olhos e a boca. Para cada um, dê um nome, uma breve descrição "
        "e o efeito esperado. Responda de forma clara, concisa e estruturada."
    )
)

# Etapa 3: Gerenciamento de sessão
session_service = InMemorySessionService()
runner = Runner(
    agent=details_agent,
    app_name="details_app",
    session_service=session_service
)
USER_ID = "user_details"
SESSION_ID = "session_details"

# Etapa 4: Executando a lógica do agente
async def execute(request):
    session_service.create_session(
        app_name="details_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    
    # Pegamos as informações que o host_agent enviou. 
    # Usamos o .get() para garantir que, se a informação não vier, usamos um valor padrão (ex: 'evento casual').
    occasion = request.get('occasion', 'evento casual')
    style = request.get('style', 'natural')
    
    prompt = (
        f"O usuário está se arrumando para a ocasião '{occasion}' com um estilo '{style}'. "
        f"Sugira 2-3 dicas de maquiagem para olhos e lábios (ex: delineado gatinho, batom vermelho). "
        f"Responda EXCLUSIVAMENTE em formato JSON, usando a chave 'details' contendo uma lista com as dicas."
    )
    
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            
            # Aqui tentamos ler o texto da IA e converter para um dicionário Python (JSON)
            try:
                parsed = json.loads(response_text)
                # Se a conversão deu certo, verificamos se a chave 'details' está lá dentro
                if "details" in parsed and isinstance(parsed["details"], list):
                    return {"details": parsed["details"]}
                else:
                    print("A chave 'details' não foi encontrada ou não é uma lista no JSON retornado.")
                    return {"details": response_text}  # Retorna o texto puro como plano B
                    
            # Se a IA não responder em formato JSON e o código falhar na conversão, o 'except' captura o erro
            # e evita que o servidor inteiro caia.
            except json.JSONDecodeError as e:
                print("Falha ao ler o JSON:", e)
                print("Conteúdo da resposta:", response_text)
                return {"details": response_text}