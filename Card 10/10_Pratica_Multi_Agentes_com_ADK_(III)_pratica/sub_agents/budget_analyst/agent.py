from datetime import datetime
from google.adk.agents import Agent

def get_travel_costs(destination: str, category: str = "general") -> dict:
    """
    Simula a busca de custos médios para um destino.
    Categorias: food, transport, attractions, general.
    """
    print(f"--- Tool: get_travel_costs called for {destination} ({category}) ---")
    
    # Mock de dados 
    costs_db = {
        "tokyo": {"food": 50, "transport": 15, "attractions": 30},
        "paris": {"food": 70, "transport": 20, "attractions": 40},
        "new york": {"food": 80, "transport": 12, "attractions": 50}
    }
    
    dest_lower = destination.lower()
    if dest_lower not in costs_db:
        return {
            "status": "error",
            "error_message": f"Dados de custo não encontrados para {destination}",
        }

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prices = costs_db[dest_lower]
    
    return {
        "status": "success",
        "destination": destination,
        "daily_budget_usd": prices.get(category, sum(prices.values())),
        "timestamp": current_time,
    }

# Definição do Agente
budget_analyst = Agent(
    name="budget_analyst",
    model="gemini-2.0-flash",
    description="Um agente que estima custos de viagem e orçamentos diários.",
    instruction="""
    Você é um assistente financeiro de viagens que ajuda usuários a planejar seus gastos.
    
    Quando perguntado sobre custos ou orçamentos:
    1. Use a ferramenta get_travel_costs para obter estimativas do destino.
    2. Formate a resposta mostrando o custo diário sugerido em dólar (USD).
    3. Informe sempre o horário em que a estimativa foi gerada.
    
    Exemplo de formato de resposta:
    "Aqui está a estimativa de custos para sua viagem:
    - Destino: Tóquio
    - Custo Diário (Alimentação): $50.00
    - Custo Diário (Transporte): $15.00
    - Atualizado em: 2026-03-13 12:00:00"
    """,
    tools=[get_travel_costs],
)