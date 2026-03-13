from pydantic import BaseModel

class MakeupRequest(BaseModel):
    skin_type: str  # Tipo de pele (ex: "mista", "oleosa", "seca")
    occasion: str   # Ocasião (ex: "casamento", "dia a dia", "festa") 
    style: str      # Estilo desejado (ex: "natural", "glam", "gótico") 