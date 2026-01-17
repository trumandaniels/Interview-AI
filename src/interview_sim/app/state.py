from pydantic import BaseModel, Field
from typing import List, Annotated, Optional
import operator
from langchain_core.messages import BaseMessage

class InterviewState(BaseModel):
    messages: Annotated[List[BaseMessage], operator.add] 
    
    job_description: str
    resume_text: str
    company_description: str
    rubric: str
    
    common_questions: List[str]

    question_count: int = 0
    max_questions: int = 5
    is_finished: bool = False
    
    final_score: Optional[int] = None
    feedback_report: Optional[str] = None