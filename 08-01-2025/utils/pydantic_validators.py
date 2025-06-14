from pydantic import BaseModel,Field
from langchain_core.prompts import PromptTemplate

from typing import List, Dict, Any, Literal,TypedDict



class SupervisorOutputparser(BaseModel):
    """Output parser for the supervisor node"""
    decision: Literal['LLM', 'RAG', 'Web Search'] = Field(
        description="The decision made by the supervisor node, indicating which model to route the query to."
    )
    
    @classmethod
    def validate_decision(cls, value: str) -> str:
        """Validate the decision to ensure it is one of the allowed values."""
        if value not in ['LLM', 'RAG', 'Web Search']:
            raise ValueError("Decision must be one of 'LLM', 'RAG', or 'Web Search'.")
        return value

class ValidationResult(BaseModel):
    is_valid: bool = Field(description="Whether the response is valid")
    confidence_score: float = Field(description="Confidence score between 0 and 1")
    issues: List[str] = Field(description="List of issues found if invalid", default=[])
    suggestion: str = Field(description="Suggestion for improvement if invalid", default="")

