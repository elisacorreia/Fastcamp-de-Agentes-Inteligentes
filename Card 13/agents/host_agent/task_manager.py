from common.a2a_client import call_agent

EXTRACTOR_URL = "http://localhost:8001/run"
SPECIALTY_URL = "http://localhost:8002/run"

async def run(payload):
    print("Processando nova transcrição médica...")
    
    
    extracao = await call_agent(EXTRACTOR_URL, payload)
    triagem = await call_agent(SPECIALTY_URL, payload)
    
    
    return {
        "status": "sucesso",
        "entidades_clinicas": extracao.get("extracted_data", {}),
        "triagem": triagem.get("classification", {})
    }