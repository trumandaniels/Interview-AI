from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form
from .graph import app_graph
from .utils.audio import transcribe_audio
from .state import InterviewState  # <--- IMPORT THIS
from langchain_core.messages import HumanMessage

app = FastAPI()

sessions = {}

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
    
    # Now input is strictly InterviewState
    events = app_graph.invoke(initial_state)
    
    # Depending on LangGraph version/config, 'events' might be a dict or State object.
    # If events is a dict (standard output), access via keys.
    # If events is InterviewState object, use dot notation.
    # Usually invoke returns a dict of the final state.
    sessions[session_id] = events 
    
    return {"response": events["messages"][-1].content} 

@app.post("/submit_answer")
async def submit_answer(
    session_id: str = Form(...),
    audio: UploadFile = File(...)
):
    user_text = await transcribe_audio(audio)
    
    # Retrieve dict from session
    current_state_dict = sessions.get(session_id)
    if not current_state_dict:
        return {"error": "Session not found"}
    
    # FIX: Re-hydrate into Pydantic model if needed, 
    # OR rely on LangGraph to accept dict at runtime (ignore type error),
    # BUT explicitly handling it is safer for types:
    
    # Update the messages list in the dict (or model)
    current_state_dict["messages"].append(HumanMessage(content=user_text))
    
    # Invoke handles dicts at runtime usually, but to fix the TYPE ERROR:
    # You would cast it: app_graph.invoke(InterviewState(**current_state_dict))
    new_state = app_graph.invoke(current_state_dict) 
    
    sessions[session_id] = new_state
    
    if new_state.get("feedback_report"):
        return {
            "status": "completed",
            "report": new_state["feedback_report"],
            "score": new_state["final_score"]
        }
    
    return {
        "status": "ongoing",
        "transcription": user_text,
        "response": new_state["messages"][-1].content
    }