from pydantic import BaseModel, Field
from typing import List, Dict


class ObserverThoughts(BaseModel):
    analysis: str = Field(default="", description="Анализ ответа кандидата")
    instructions: str = Field(description="Инструкция для интервьюера")
    is_hallucination: bool = Field(description="Врет ли кандидат?")
    current_stage: str = Field(description="Intro / Basics / Deep Tech / Soft Skills / Closing")

class FinalReport(BaseModel):
    grade: str = Field(description="Junior/Middle/Senior")
    recommendation: str = Field(description="Hire/No Hire")
    confidence_score: int = Field(description="0-100")
    confirmed_skills: List[str]
    knowledge_gaps: List[Dict[str, str]] 
    Clarity: str
    Honesty: str
    Engagement: str
    roadmap: List[str]