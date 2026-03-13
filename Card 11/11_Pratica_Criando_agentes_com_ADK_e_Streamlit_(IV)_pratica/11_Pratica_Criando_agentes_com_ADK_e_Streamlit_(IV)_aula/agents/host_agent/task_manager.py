from common.a2a_client import call_agent

SKINCARE_URL = "http://localhost:8001/run"
BASE_MAKEUP_URL = "http://localhost:8002/run"
DETAILS_URL = "http://localhost:8003/run"

async def run(payload):
    print("Dados recebidos do usuário:", payload)
    
    # Chamando cada especialista
    skincare = await call_agent(SKINCARE_URL, payload)
    base_makeup = await call_agent(BASE_MAKEUP_URL, payload)
    details = await call_agent(DETAILS_URL, payload)
    
    print("Skincare:", skincare)
    print("Base:", base_makeup)
    print("Detalhes:", details)
    
    skincare = skincare if isinstance(skincare, dict) else {}
    base_makeup = base_makeup if isinstance(base_makeup, dict) else {}
    details = details if isinstance(details, dict) else {}
    
    # Juntando as recomendações e devolvendo
    return {
        "skincare": skincare.get("skincare", "Nenhuma dica de pele retornada."),
        "base_makeup": base_makeup.get("base_makeup", "Nenhuma dica de base retornada."),
        "details": details.get("details", "Nenhuma dica de olhos/boca retornada.")
    }