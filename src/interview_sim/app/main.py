from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form
from .graph import app_graph
from .utils.audio import transcribe_audio
from .state import InterviewState 
from langchain_core.messages import HumanMessage

app = FastAPI()

@app.post("/start_interview")
async def start_interview(
    resume: str = Form(...),
    job_desc: str = Form(...),
    rubric: str = Form(...),
    session_id: str = Form(...)
):
    initial_state = InterviewState(
        messages=[],
        job_description=job_desc,
        company_description="TechCorp Inc.",
        resume_text=resume,
        rubric=rubric,
        common_questions=["Tell me about yourself", "Weaknesses?", "Hardest bug?"],
        question_count=0,
        max_questions=5,
        is_finished=False
    )
    
    config = {"configurable": {"thread_id": session_id}}
    events = app_graph.invoke(initial_state, config=config)

    return {"response": events["messages"][-1].content} 

@app.post("/submit_answer")
async def submit_answer(
    session_id: str = Form(...),
    audio: UploadFile = File(...)
):
    user_text = await transcribe_audio(audio)
    
    update_data = {"messages": [HumanMessage(content=user_text)]}
    
    config = {"configurable": {"thread_id": session_id}}
    new_state = app_graph.invoke(update_data, config=config) 
    
    if new_state.get("feedback_report"):
        return {
            "status": "completed",
            "report": new_state["feedback_report"],
            "score": new_state.get("final_score", 0)
        }
    
    return {
        "status": "ongoing",
        "transcription": user_text,
        "response": new_state["messages"][-1].content
    }