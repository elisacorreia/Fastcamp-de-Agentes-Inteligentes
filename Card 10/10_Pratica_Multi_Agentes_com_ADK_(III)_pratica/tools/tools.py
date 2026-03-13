from datetime import datetime

def get_current_time() -> dict:
    """
    Retorna a data e hora atual. Útil para contextualizar roteiros e eventos sazonais.
    """
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """
    Converte valores entre moedas (Simulação). 
    Útil para o budget_analyst calcular gastos em moedas locais.
    """
    # Taxas de conversão 
    rates = {
        "USD_BRL": 5.0,
        "USD_JPY": 150.0,
        "USD_EUR": 0.92,
        "BRL_USD": 0.20
    }
    
    pair = f"{from_currency.upper()}_{to_currency.upper()}"
    rate = rates.get(pair, 1.0)
    converted_amount = amount * rate
    
    return {
        "original_amount": amount,
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "converted_amount": round(converted_amount, 2),
        "rate_used": rate
    }