from pydantic import BaseModel

class TranscriptionRequest(BaseModel):
    transcription_text: str  