from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def get_destination_info(city: str, tool_context: ToolContext) -> dict:
    """Simula a busca de atrações e logística para uma cidade."""
    print(f"--- Tool: get_destination_info called for: {city} ---")

    # Base de dados de exemplo para o roteiro
    destinations = {
        "tóquio": "Sugestão: Manhã em Akihabara, Tarde no Templo Senso-ji. Transporte: JR Pass / Metrô.",
        "paris": "Sugestão: Manhã na Torre Eiffel, Tarde no Museu do Louvre. Transporte: Metrô / Caminhada.",
        "nova york": "Sugestão: Manhã no Central Park, Tarde na Times Square. Transporte: Subway.",
        "default": "Sugestão: Explore o centro histórico e utilize transporte público local."
    }

    info = destinations.get(city.lower(), destinations["default"])
    
    # Salva a última cidade pesquisada no contexto
    tool_context.state["last_city_planned"] = city

    return {
        "status": "success", 
        "info": info, 
        "city": city
    }

# Definição do agente 
itinerary_specialist = Agent(
    name="itinerary_specialist",
    model="gemini-2.0-flash",
    description="Um agente que cria roteiros de viagem e sugere logística de transporte.",
    instruction="""
    Você é um Especialista em Roteiros de Viagem.
    
    Sua missão é ajudar o usuário a organizar o que fazer em cada cidade.
    1. Use a ferramenta get_destination_info para obter sugestões baseadas na cidade.
    2. Se o usuário não mencionar uma cidade, pergunte para onde ele deseja viajar.
    3. Formate a resposta com uma sugestão de manhã e tarde, incluindo a melhor forma de se locomover.
    
    Exemplo de resposta:
    "Para sua viagem a [Cidade]:
    - Planejamento: [Sugestão da Ferramenta]
    - Dica extra: Tente reservar ingressos com antecedência para evitar filas."
    """,
    tools=[get_destination_info],
)