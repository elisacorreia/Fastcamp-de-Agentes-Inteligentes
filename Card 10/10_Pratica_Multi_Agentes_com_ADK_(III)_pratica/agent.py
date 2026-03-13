from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

# Importação simplificada 
from .sub_agents import budget_analyst, itinerary_specialist, news_analyst
from .tools.tools import get_current_time

root_agent = Agent(
    name="travel_manager",
    model="gemini-2.0-flash",
    description="Gestor de Viagens Inteligente",
    instruction="""
    Você é um Gestor de Viagens responsável por coordenar o planeamento completo de uma viagem.

    Sua função é entender o pedido do utilizador e delegar para o especialista correto:
    1. Delegue para o 'budget_analyst' quando o assunto for custos, moedas, orçamentos ou preços.
    2. Delegue para o 'itinerary_specialist' para criar roteiros, escolher atrações e decidir meios de transporte.
    3. Use o 'news_analyst' como ferramenta para verificar eventos em tempo real, festivais ou notícias locais que possam impactar a viagem.

    Fluxo de Trabalho Ideal:
    - Se o utilizador quiser planear uma viagem do zero, peça primeiro ao 'itinerary_specialist' para sugerir locais.
    - Depois, peça ao 'budget_analyst' para estimar os custos desses locais.
    - Por fim, consulte o 'news_analyst' para garantir que não existem feriados ou eventos que fechem as atrações.

    Utilize a ferramenta 'get_current_time' para saber a data atual e contextulizar as pesquisas.
    """,
    sub_agents=[budget_analyst, itinerary_specialist],
    tools=[
        AgentTool(news_analyst),
        get_current_time,
    ],
)